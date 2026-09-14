"""Preview-first, deterministic repository file controls."""
import base64
import hashlib
import json
import re
import os
import subprocess
import time
from pathlib import Path
from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from pydantic import BaseModel, Field
from .main import current_user, database, uid

router=APIRouter(prefix='/api/v1/hub')
SKIP={'.git','node_modules','.venv','venv','dist','build','__pycache__'}
BLOCKED={'.env','.env.local','.env.production','credentials.json','secrets.json'}
TEXT_EXT={'.txt','.md','.html','.css','.scss','.js','.jsx','.ts','.tsx','.json','.py','.php','.sql','.xml','.yml','.yaml','.java','.c','.cpp','.h','.sh','.ps1','.cmd'}

class CommandInput(BaseModel):command:str=Field(min_length=3,max_length=2000)
class CommitInput(BaseModel):message:str=Field(min_length=3,max_length=200)
class FileSaveInput(BaseModel):
    path:str=Field(min_length=1,max_length=1000)
    content:str=Field(max_length=2_000_000)
    expected_hash:str|None=None
class QuickPushInput(BaseModel):
    message:str=Field(min_length=3,max_length=200)
class CloneInput(BaseModel):
    repository_url:str=Field(min_length=10,max_length=500)
    destination_parent:str=Field(min_length=1,max_length=1000)

def project_root(project_id,user_id):
    with database() as db:row=db.execute('SELECT local_path FROM hub_projects WHERE id=? AND user_id=?',(project_id,user_id)).fetchone()
    if not row:raise HTTPException(404,'Project not found')
    root=Path(row['local_path']).expanduser().resolve() if row['local_path'] else None
    if not root or not root.is_dir() or not (root/'.git').exists():raise HTTPException(400,'Connect a valid local Git repository folder first')
    return root

def safe_path(root,relative):
    relative=relative.strip().strip('"\'').replace('\\','/')
    if not relative or Path(relative).is_absolute():raise HTTPException(400,'Use a path relative to the repository')
    target=(root/relative).resolve()
    if root not in target.parents or any(p in SKIP for p in target.relative_to(root).parts) or target.name.lower() in BLOCKED or target.name.lower().startswith('.env'):
        raise HTTPException(403,'That path is protected')
    return target

def digest(path):return hashlib.sha256(path.read_bytes()).hexdigest() if path.exists() else None

def git(root,*args,timeout=20):
    try:
        return subprocess.run(['git','-C',str(root),*args],capture_output=True,text=True,timeout=timeout,check=False)
    except (OSError,subprocess.TimeoutExpired) as exc:
        raise HTTPException(503,'Git is unavailable or did not respond in time') from exc

def repo_status(root):
    branch=git(root,'branch','--show-current').stdout.strip() or 'detached HEAD'
    remote=git(root,'remote','get-url','origin').stdout.strip()
    lines=git(root,'status','--porcelain=v1').stdout.splitlines()
    files=[]
    for line in lines[:500]:
        path=line[3:].split(' -> ')[-1]
        files.append({'path':path,'status':line[:2].strip() or 'modified','blocked':is_secret_path(path) or contains_secret(root/path)})
    upstream=git(root,'rev-parse','--abbrev-ref','--symbolic-full-name','@{u}')
    ahead=behind=0
    if upstream.returncode==0:
        counts=git(root,'rev-list','--left-right','--count','HEAD...@{u}').stdout.strip().split()
        if len(counts)==2:ahead,behind=(int(counts[0]),int(counts[1]))
    return {'branch':branch,'remote':remote,'files':files,'changed':len(lines),'ahead':ahead,'behind':behind,'has_upstream':upstream.returncode==0}

def is_secret_path(relative):
    parts=Path(relative.replace('\\','/')).parts
    name=parts[-1].lower() if parts else ''
    return name in BLOCKED or name.startswith('.env') or name.endswith(('.pem','.key','.p12','.pfx')) or any(p.lower() in {'credentials','secrets'} for p in parts)

def contains_secret(path):
    """Conservative scan for recognizable secret values without returning them."""
    if not path.is_file() or path.suffix.lower() not in TEXT_EXT or path.stat().st_size>2_000_000:return False
    try:text=path.read_text(encoding='utf-8')
    except (OSError,UnicodeDecodeError):return False
    patterns=(
        r'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----',
        r'\bgh[pousr]_[A-Za-z0-9]{20,}\b',
        r'\bAKIA[A-Z0-9]{16}\b',
        r'(?i)\b(?:api[_-]?key|access[_-]?token|client[_-]?secret)\b\s*[:=]\s*["\'][^"\'\s]{20,}["\']',
    )
    return any(re.search(pattern,text) for pattern in patterns)

@router.post('/system/pick-folder')
def pick_folder(user=Depends(current_user)):
    """Open the operating system folder chooser for this local desktop instance."""
    if os.name!='nt':raise HTTPException(501,'Folder selection is available in the Windows desktop app')
    try:
        import tkinter as tk
        from tkinter import filedialog
        root=tk.Tk();root.withdraw();root.attributes('-topmost',True)
        selected=filedialog.askdirectory(title='Choose a project or destination folder')
        root.destroy()
    except Exception as exc:raise HTTPException(500,'Windows could not open the folder chooser') from exc
    return {'path':selected}

@router.post('/projects/{project_id}/repo/clone')
def clone_repository(project_id:str,body:CloneInput,user=Depends(current_user)):
    if not re.fullmatch(r'https://github\.com/[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+(?:\.git)?/?',body.repository_url):
        raise HTTPException(422,'Use a valid HTTPS GitHub repository URL')
    parent=Path(body.destination_parent).expanduser().resolve()
    if not parent.is_dir():raise HTTPException(400,'Choose an existing destination folder')
    repo_name=body.repository_url.rstrip('/').rsplit('/',1)[-1].removesuffix('.git')
    destination=parent/repo_name
    if destination.exists():raise HTTPException(409,f'{destination} already exists')
    try:result=subprocess.run(['git','clone','--',body.repository_url,str(destination)],capture_output=True,text=True,timeout=180,check=False)
    except (OSError,subprocess.TimeoutExpired) as exc:raise HTTPException(503,'Git clone could not start or timed out') from exc
    if result.returncode:raise HTTPException(400,(result.stderr or 'Git clone failed')[-1000:])
    with database() as db:
        changed=db.execute('UPDATE hub_projects SET local_path=?,repository_url=?,updated_at=? WHERE id=? AND user_id=?',(str(destination),body.repository_url,time.time(),project_id,user['id'])).rowcount
        if not changed:raise HTTPException(404,'Project not found')
    return {'ok':True,'local_path':str(destination),'repository_url':body.repository_url}

@router.get('/projects/{project_id}/repo/status')
def repository_status(project_id:str,user=Depends(current_user)):
    status=repo_status(project_root(project_id,user['id']))
    with database() as db:
        row=db.execute(
            "SELECT created_at FROM hub_repo_actions WHERE project_id=? AND user_id=? AND kind='quick_push' AND status='applied' ORDER BY created_at DESC LIMIT 1",
            (project_id,user['id']),
        ).fetchone()
    status['last_push_at']=row['created_at'] if row else None
    return status

@router.post('/projects/{project_id}/repo/open-vscode')
def open_in_vscode(project_id:str,user=Depends(current_user)):
    """Open the connected repository in VS Code without accepting a shell command."""
    root=project_root(project_id,user['id'])
    try:
        subprocess.Popen(['code',str(root)],cwd=str(root),stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
    except OSError as exc:
        raise HTTPException(503,'VS Code command is unavailable. Install VS Code and enable the code command.') from exc
    return {'ok':True,'message':'Opened the repository in VS Code'}

@router.get('/projects/{project_id}/repo/files')
def repository_files(project_id:str,path:str='',user=Depends(current_user)):
    root=project_root(project_id,user['id']);folder=root if not path else safe_path(root,path)
    if not folder.is_dir():raise HTTPException(404,'Folder not found')
    entries=[]
    for item in sorted(folder.iterdir(),key=lambda p:(not p.is_dir(),p.name.casefold())):
        relative=str(item.relative_to(root)).replace('\\','/')
        if item.name in SKIP or is_secret_path(relative):continue
        entries.append({'name':item.name,'path':relative,'type':'folder' if item.is_dir() else 'file','editable':item.is_file() and item.suffix.lower() in TEXT_EXT and item.stat().st_size<=2_000_000})
        if len(entries)>=500:break
    return {'path':path,'entries':entries}

@router.get('/projects/{project_id}/repo/file')
def repository_file(project_id:str,path:str,user=Depends(current_user)):
    root=project_root(project_id,user['id']);target=safe_path(root,path)
    if not target.is_file() or target.suffix.lower() not in TEXT_EXT:raise HTTPException(404,'Editable text file not found')
    if target.stat().st_size>2_000_000:raise HTTPException(413,'File is larger than 2 MB')
    try:content=target.read_text(encoding='utf-8')
    except UnicodeDecodeError as exc:raise HTTPException(422,'File is not UTF-8 text') from exc
    return {'path':str(target.relative_to(root)).replace('\\','/'),'content':content,'hash':digest(target),'size':target.stat().st_size}

@router.post('/projects/{project_id}/repo/file-plan')
def plan_file_save(project_id:str,body:FileSaveInput,user=Depends(current_user)):
    root=project_root(project_id,user['id']);target=safe_path(root,body.path)
    if target.suffix.lower() not in TEXT_EXT:raise HTTPException(422,'This file type is not editable')
    current=digest(target)
    if body.expected_hash!=current:raise HTTPException(409,'File changed since it was opened; reload it')
    old=target.read_text(encoding='utf-8') if target.exists() else ''
    changed_lines=sum(a!=b for a,b in zip(old.splitlines(),body.content.splitlines()))+abs(len(old.splitlines())-len(body.content.splitlines()))
    relative=str(target.relative_to(root)).replace('\\','/')
    return save_action(user['id'],project_id,'file_save',{'path':relative,'content':body.content,'hash':current},{'summary':f'Save {relative} ({changed_lines} changed line(s))','files':[{'path':relative,'count':changed_lines}]})

@router.post('/projects/{project_id}/repo/quick-push-plan')
def plan_quick_push(project_id:str,body:QuickPushInput,user=Depends(current_user)):
    root=project_root(project_id,user['id']);status=repo_status(root)
    if not status['files']:raise HTTPException(409,'There are no local changes to push')
    blocked=[f['path'] for f in status['files'] if f['blocked']]
    if blocked:raise HTTPException(403,'Remove protected secret files from the changes before pushing: '+', '.join(blocked[:5]))
    if not status['remote']:raise HTTPException(409,'Connect an origin remote before pushing')
    signature=hashlib.sha256(json.dumps(status['files'],sort_keys=True).encode()).hexdigest()
    return save_action(user['id'],project_id,'quick_push',{'message':body.message,'signature':signature},{'summary':f'Commit {status["changed"]} changed file(s) and push {status["branch"]} to origin','files':status['files'][:100],'branch':status['branch'],'remote':status['remote'],'message':body.message})

def save_action(user_id,project_id,kind,payload,preview):
    ident=uid();payload['preview']=preview
    with database() as db:db.execute('INSERT INTO hub_repo_actions VALUES(?,?,?,?,?,?,?)',(ident,user_id,project_id,kind,json.dumps(payload), 'pending',time.time()))
    return {'action_id':ident,'kind':kind,'preview':preview,'requires_approval':True}

@router.post('/projects/{project_id}/repo/plan')
def plan_command(project_id:str,body:CommandInput,user=Depends(current_user)):
    root=project_root(project_id,user['id']);command=' '.join(body.command.strip().split())
    match=re.match(r'^commit (?:these )?changes as\s+["\']?(.+?)["\']?$',command,re.I)
    if match:
        message=match.group(1).strip('"\' ');status=subprocess.run(['git','-C',str(root),'status','--short'],capture_output=True,text=True,timeout=10,check=False).stdout
        if not status:raise HTTPException(409,'There are no changes to commit')
        return save_action(user['id'],project_id,'git_commit',{'message':message}, {'summary':f'Commit current changes as: {message}','files':[{'path':line[3:]} for line in status.splitlines()[:100]]})
    if re.match(r'^push (?:the )?(?:current )?branch$',command,re.I):
        branch=subprocess.run(['git','-C',str(root),'branch','--show-current'],capture_output=True,text=True,timeout=10,check=False).stdout.strip()
        return save_action(user['id'],project_id,'git_push',{}, {'summary':f'Push branch {branch or "current branch"} to its configured remote','files':[]})
    match=re.match(r'^replace\s+["\']?(.+?)["\']?\s+with\s+["\']?(.+?)["\']?\s+(?:everywhere|in all files)(?:\s+in\s+.+)?$',command,re.I)
    if match:
        old,new=match.group(1).strip('"\''),match.group(2).strip('"\'');changes=[];total=0
        if not old:raise HTTPException(422,'The search text cannot be empty')
        for path in root.rglob('*'):
            if not path.is_file() or path.suffix.lower() not in TEXT_EXT or any(p in SKIP for p in path.relative_to(root).parts) or path.stat().st_size>2_000_000:continue
            try:text=path.read_text(encoding='utf-8')
            except UnicodeDecodeError:continue
            count=text.count(old)
            if count:changes.append({'path':str(path.relative_to(root)).replace('\\','/'),'count':count,'hash':digest(path)});total+=count
            if len(changes)>500:raise HTTPException(413,'More than 500 files matched; narrow the command')
        return save_action(user['id'],project_id,'replace',{'old':old,'new':new,'changes':changes}, {'summary':f'Replace {total} occurrence(s) in {len(changes)} file(s)','files':changes[:100]})
    match=re.match(r'^replace\s+["\']?(.+?)["\']?\s+with\s+["\']?(.+?)["\']?\s+in\s+(.+)$',command,re.I)
    if match:
        old,new,relative=match.group(1).strip('"\''),match.group(2).strip('"\''),match.group(3);path=safe_path(root,relative)
        if not path.is_file() or path.suffix.lower() not in TEXT_EXT:raise HTTPException(404,'Editable text file not found')
        text=path.read_text(encoding='utf-8');count=text.count(old);change={'path':str(path.relative_to(root)).replace('\\','/'),'count':count,'hash':digest(path)}
        return save_action(user['id'],project_id,'replace',{'old':old,'new':new,'changes':[change]}, {'summary':f'Replace {count} occurrence(s) in {change["path"]}','files':[change]})
    match=re.match(r'^(?:delete|remove)\s+(?:file\s+)?(.+)$',command,re.I)
    if match:
        path=safe_path(root,match.group(1));
        if not path.is_file():raise HTTPException(404,'File not found')
        relative=str(path.relative_to(root)).replace('\\','/')
        return save_action(user['id'],project_id,'delete',{'path':relative,'hash':digest(path)}, {'summary':f'Delete {relative}','files':[{'path':relative}]})
    raise HTTPException(422,'Use: replace OLD with NEW everywhere; replace OLD with NEW in PATH; or delete PATH')

@router.post('/projects/{project_id}/repo/upload-plan')
async def plan_upload(project_id:str,target_path:str=Form(...),file:UploadFile=File(...),user=Depends(current_user)):
    root=project_root(project_id,user['id']);target=safe_path(root,target_path);raw=await file.read(2_000_001)
    if len(raw)>2_000_000:raise HTTPException(413,'Maximum upload size is 2 MB')
    relative=str(target.relative_to(root)).replace('\\','/');exists=target.exists()
    return save_action(user['id'],project_id,'upload',{'path':relative,'content':base64.b64encode(raw).decode(),'hash':digest(target)}, {'summary':('Replace' if exists else 'Add')+f' {relative}','files':[{'path':relative,'uploaded_name':Path(file.filename or 'upload').name,'overwrites':exists}]})

@router.post('/repo-actions/{action_id}/apply')
def apply_action(action_id:str,user=Depends(current_user)):
    with database() as db:row=db.execute("SELECT * FROM hub_repo_actions WHERE id=? AND user_id=? AND status='pending'",(action_id,user['id'])).fetchone()
    if not row:raise HTTPException(404,'Pending action not found')
    if time.time()-row['created_at']>1800:raise HTTPException(410,'Preview expired; create it again')
    root=project_root(row['project_id'],user['id']);payload=json.loads(row['payload']);kind=row['kind'];changed=[]
    if kind=='replace':
        for item in payload['changes']:
            path=safe_path(root,item['path'])
            if digest(path)!=item['hash']:raise HTTPException(409,f'{item["path"]} changed after preview')
        for item in payload['changes']:
            path=safe_path(root,item['path']);text=path.read_text(encoding='utf-8');path.write_text(text.replace(payload['old'],payload['new']),encoding='utf-8');changed.append(item['path'])
    elif kind=='delete':
        path=safe_path(root,payload['path'])
        if digest(path)!=payload['hash']:raise HTTPException(409,'File changed after preview')
        path.unlink();changed=[payload['path']]
    elif kind=='upload':
        path=safe_path(root,payload['path'])
        if digest(path)!=payload['hash']:raise HTTPException(409,'Destination changed after preview')
        path.parent.mkdir(parents=True,exist_ok=True);path.write_bytes(base64.b64decode(payload['content']));changed=[payload['path']]
    elif kind=='file_save':
        path=safe_path(root,payload['path'])
        if digest(path)!=payload['hash']:raise HTTPException(409,'File changed after preview')
        path.parent.mkdir(parents=True,exist_ok=True);path.write_text(payload['content'],encoding='utf-8');changed=[payload['path']]
    elif kind=='git_commit':
        subprocess.run(['git','-C',str(root),'add','-A'],capture_output=True,text=True,timeout=20,check=True)
        result=subprocess.run(['git','-C',str(root),'commit','-m',payload['message']],capture_output=True,text=True,timeout=30,check=False)
        if result.returncode:raise HTTPException(400,(result.stderr or result.stdout or 'Git commit failed')[-1000:])
        changed=['Git commit created']
    elif kind=='git_push':
        result=subprocess.run(['git','-C',str(root),'push'],capture_output=True,text=True,timeout=60,check=False)
        if result.returncode:raise HTTPException(400,(result.stderr or result.stdout or 'Git push failed')[-1000:])
        changed=['Current branch pushed']
    elif kind=='quick_push':
        status=repo_status(root)
        signature=hashlib.sha256(json.dumps(status['files'],sort_keys=True).encode()).hexdigest()
        if signature!=payload['signature']:raise HTTPException(409,'Repository changed after confirmation; review it again')
        if any(f['blocked'] for f in status['files']):raise HTTPException(403,'Protected secret file detected; push stopped')
        fetch=git(root,'fetch','origin',timeout=60)
        if fetch.returncode:raise HTTPException(400,(fetch.stderr or 'Could not check the remote repository')[-1000:])
        upstream=git(root,'rev-parse','--abbrev-ref','--symbolic-full-name','@{u}')
        if upstream.returncode==0:
            counts=git(root,'rev-list','--left-right','--count','HEAD...@{u}').stdout.strip().split()
            if len(counts)==2 and int(counts[1])>0:raise HTTPException(409,'Remote contains newer commits. Pull and resolve them before pushing')
        else:
            branch=git(root,'branch','--show-current').stdout.strip()
            remote_ref=f'origin/{branch}'
            if branch and git(root,'rev-parse','--verify',remote_ref).returncode==0:
                counts=git(root,'rev-list','--left-right','--count',f'HEAD...{remote_ref}').stdout.strip().split()
                if len(counts)==2 and int(counts[1])>0:raise HTTPException(409,'Remote contains newer commits. Pull and resolve them before pushing')
        added=git(root,'add','-A')
        if added.returncode:raise HTTPException(400,(added.stderr or 'Could not stage changes')[-1000:])
        committed=git(root,'commit','-m',payload['message'],timeout=30)
        if committed.returncode:raise HTTPException(400,(committed.stderr or committed.stdout or 'Git commit failed')[-1000:])
        branch=git(root,'branch','--show-current').stdout.strip()
        if not branch:raise HTTPException(409,'Choose a branch before using Quick Push')
        push_args=('push',) if upstream.returncode==0 else ('push','-u','origin',branch)
        pushed=git(root,*push_args,timeout=90)
        if pushed.returncode:raise HTTPException(400,(pushed.stderr or pushed.stdout or 'Git push failed')[-1000:])
        changed=['Changes committed and pushed successfully']
    with database() as db:db.execute("UPDATE hub_repo_actions SET status='applied' WHERE id=?",(action_id,))
    return {'applied':True,'files':changed,'recovery':'Use Git restore before committing if the result is wrong.'}

@router.post('/repo-actions/{action_id}/reject')
def reject_action(action_id:str,user=Depends(current_user)):
    with database() as db:
        if not db.execute("UPDATE hub_repo_actions SET status='rejected' WHERE id=? AND user_id=? AND status='pending'",(action_id,user['id'])).rowcount:raise HTTPException(404,'Pending action not found')
    return {'rejected':True}
