from __future__ import annotations
import json, os, re, shutil, subprocess, sys, threading, uuid, webbrowser
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from pathlib import Path
from urllib.parse import parse_qs, urlparse

ROOT=Path(__file__).resolve().parent
DATA=Path(os.environ.get("LOCALAPPDATA",ROOT))/"AwareMinds"
CONFIG=DATA/"workspace.json"
HOST,PORT="127.0.0.1",8765
TEXT_EXT={".html",".css",".js",".mjs",".cjs",".ts",".tsx",".jsx",".json",".md",".txt",".py",".php",".java",".c",".cpp",".h",".cs",".go",".rs",".rb",".sql",".xml",".yaml",".yml",".toml",".ini",".env.example"}
BLOCKED={".git","node_modules",".next","dist","build",".venv","venv","__pycache__",".idea"}
SECRET_NAMES={".env","id_rsa","id_ed25519","credentials.json","service-account.json"}
MAX_FILE=2*1024*1024

def load_config():
    DATA.mkdir(parents=True,exist_ok=True)
    try:return json.loads(CONFIG.read_text("utf-8"))
    except Exception:return {"projects":{}}
CFG=load_config()
def save_config():
    DATA.mkdir(parents=True,exist_ok=True)
    tmp=CONFIG.with_suffix(".tmp");tmp.write_text(json.dumps(CFG,indent=2),"utf-8");tmp.replace(CONFIG)
def run(args,cwd,timeout=60):
    p=subprocess.run(args,cwd=cwd,text=True,capture_output=True,timeout=timeout,creationflags=getattr(subprocess,"CREATE_NO_WINDOW",0))
    if p.returncode:raise RuntimeError((p.stderr or p.stdout or "Command failed").strip())
    return p.stdout.strip()
def project(pid):
    raw=CFG.get("projects",{}).get(pid)
    if not raw:raise ValueError("Project folder is not connected on this computer.")
    p=Path(raw).resolve()
    if not p.is_dir():raise ValueError("Connected project folder no longer exists.")
    return p
def safe_file(root,rel):
    if not isinstance(rel,str) or not rel or "\x00" in rel:raise ValueError("Invalid file path.")
    target=(root/rel).resolve()
    try:target.relative_to(root)
    except ValueError:raise ValueError("Path must stay inside the project.")
    if any(x in BLOCKED for x in target.parts) or target.name.lower() in SECRET_NAMES:raise ValueError("Protected files cannot be opened.")
    if target.suffix.lower() not in TEXT_EXT:raise ValueError("Only recognized text source files can be edited.")
    return target
def pick_folder(title):
    try:
        import tkinter as tk
        from tkinter import filedialog
        root=tk.Tk();root.withdraw();root.attributes("-topmost",True)
        value=filedialog.askdirectory(title=title);root.destroy();return value
    except Exception as e:raise RuntimeError("Windows folder picker is unavailable: "+str(e))
def git_root(path):
    try:return Path(run(["git","-C",str(path),"rev-parse","--show-toplevel"],ROOT)).resolve()
    except Exception:raise ValueError("The connected folder is not a Git repository.")
class Handler(SimpleHTTPRequestHandler):
    server_version="AwareMinds/1.0"
    def translate_path(self,path):
        clean=urlparse(path).path
        if clean=="/":clean="/index.html"
        return str((ROOT/clean.lstrip("/")).resolve())
    def end_headers(self):
        self.send_header("X-Content-Type-Options","nosniff")
        self.send_header("Referrer-Policy","no-referrer")
        self.send_header("Content-Security-Policy","default-src 'self'; img-src 'self' data:; style-src 'self'; script-src 'self'; connect-src 'self'; object-src 'none'; base-uri 'none'; frame-ancestors 'none'")
        super().end_headers()
    def json(self,status,data):
        body=json.dumps(data).encode();self.send_response(status);self.send_header("Content-Type","application/json");self.send_header("Content-Length",str(len(body)));self.end_headers();self.wfile.write(body)
    def body(self):
        length=int(self.headers.get("Content-Length","0"))
        if length>MAX_FILE+4096:raise ValueError("Request is too large.")
        return json.loads(self.rfile.read(length) or b"{}")
    def do_GET(self):
        u=urlparse(self.path)
        if not u.path.startswith("/api/"):return super().do_GET()
        try:
            q=parse_qs(u.query);pid=q.get("id",[""])[0]
            if u.path=="/api/health":return self.json(200,{"ok":True,"version":"1.0.0"})
            if u.path=="/api/tree":
                root=project(pid);files=[]
                for base,dirs,names in os.walk(root):
                    dirs[:]=[d for d in dirs if d not in BLOCKED and not d.startswith(".")]
                    for name in names:
                        p=Path(base)/name
                        if p.name.lower() in SECRET_NAMES or p.suffix.lower() not in TEXT_EXT:continue
                        try:
                            if p.stat().st_size<=MAX_FILE:files.append(p.relative_to(root).as_posix())
                        except OSError:pass
                        if len(files)>=1000:break
                    if len(files)>=1000:break
                return self.json(200,{"files":sorted(files)})
            if u.path=="/api/file":
                root=project(pid);target=safe_file(root,q.get("path",[""])[0])
                if not target.is_file():raise ValueError("File does not exist.")
                if target.stat().st_size>MAX_FILE:raise ValueError("File exceeds the 2 MB editor limit.")
                return self.json(200,{"content":target.read_text("utf-8"),"path":target.relative_to(root).as_posix()})
            if u.path=="/api/git/status":
                root=git_root(project(pid))
                run(["git","fetch","--quiet"],root,25)
                branch=run(["git","branch","--show-current"],root) or "(detached)"
                raw=run(["git","status","--porcelain=v1"],root)
                files=[{"status":line[:2].strip() or "?", "path":line[3:]} for line in raw.splitlines() if line]
                ahead=behind=0
                try:
                    counts=run(["git","rev-list","--left-right","--count","HEAD...@{upstream}"],root).split()
                    ahead,behind=int(counts[0]),int(counts[1])
                except Exception:pass
                return self.json(200,{"branch":branch,"files":files,"ahead":ahead,"behind":behind})
            self.json(404,{"error":"Unknown endpoint."})
        except Exception as e:self.json(400,{"error":str(e)})
    def do_POST(self):
        try:
            data=self.body();path=urlparse(self.path).path
            if path=="/api/pick":
                pid=str(data.get("id",""))
                if not pid:raise ValueError("Missing project id.")
                chosen=pick_folder("Choose a project folder")
                if not chosen:return self.json(200,{"cancelled":True})
                resolved=str(Path(chosen).resolve());CFG.setdefault("projects",{})[pid]=resolved;save_config()
                return self.json(200,{"cancelled":False,"path":resolved})
            if path=="/api/file":
                root=project(str(data.get("id","")));target=safe_file(root,str(data.get("path","")));content=data.get("content")
                if not isinstance(content,str):raise ValueError("File content must be text.")
                if len(content.encode())>MAX_FILE:raise ValueError("File exceeds the 2 MB editor limit.")
                if not target.exists():raise ValueError("Creating new files requires the dedicated upload flow.")
                backup=DATA/"undo"/str(data.get("id",""));backup.mkdir(parents=True,exist_ok=True)
                (backup/"last.json").write_text(json.dumps({"path":str(data.get("path","")),"content":target.read_text("utf-8")}),"utf-8")
                tmp=target.with_suffix(target.suffix+".aware-tmp");tmp.write_text(content,"utf-8");tmp.replace(target)
                return self.json(200,{"saved":True})
            if path=="/api/open-vscode":
                root=project(str(data.get("id","")))
                subprocess.Popen(["code",str(root)],creationflags=getattr(subprocess,"CREATE_NO_WINDOW",0))
                return self.json(200,{"opened":True})
            if path=="/api/clone":
                url=str(data.get("url","")).strip()
                if not re.fullmatch(r"https://github\.com/[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+(?:\.git)?",url):raise ValueError("Enter a valid HTTPS GitHub repository URL.")
                parent=pick_folder("Choose a folder that will contain the repository")
                if not parent:return self.json(200,{"cancelled":True})
                name=url.rstrip("/").rsplit("/",1)[-1].removesuffix(".git");dest=Path(parent)/name
                if dest.exists():raise ValueError("A folder with this repository name already exists.")
                run(["git","clone","--",url,str(dest)],ROOT,180)
                pid=str(uuid.uuid4());CFG.setdefault("projects",{})[pid]=str(dest.resolve());save_config()
                return self.json(200,{"cancelled":False,"id":pid,"name":name,"path":str(dest.resolve())})
            if path=="/api/git/push":
                root=git_root(project(str(data.get("id",""))));message=str(data.get("message","")).strip()
                if len(message)<3 or len(message)>100:raise ValueError("Commit message must be 3–100 characters.")
                run(["git","fetch","--quiet"],root,30)
                try:
                    counts=run(["git","rev-list","--left-right","--count","HEAD...@{upstream}"],root).split()
                    if int(counts[1])>0:raise ValueError("Remote changes exist. Pull and resolve them before pushing.")
                except RuntimeError:pass
                status=run(["git","status","--porcelain=v1"],root)
                if not status:raise ValueError("There are no changes to commit.")
                blocked=[]
                for line in status.splitlines():
                    rel=line[3:]
                    if Path(rel).name.lower() in SECRET_NAMES or any(k in rel.lower() for k in ("secret","credential",".pem",".key")):blocked.append(rel)
                if blocked:raise ValueError("Push blocked because possible secret files are present: "+", ".join(blocked[:5]))
                run(["git","add","--all"],root);run(["git","commit","-m",message],root,60);run(["git","push"],root,120)
                return self.json(200,{"message":"Committed and pushed to GitHub."})
            self.json(404,{"error":"Unknown endpoint."})
        except Exception as e:self.json(400,{"error":str(e)})
    def log_message(self,fmt,*args):pass
def main():
    os.chdir(ROOT)
    try:httpd=ThreadingHTTPServer((HOST,PORT),Handler)
    except OSError:
        webbrowser.open(f"http://{HOST}:{PORT}");return
    threading.Timer(.6,lambda:webbrowser.open(f"http://{HOST}:{PORT}")).start()
    print(f"Aware Minds is running at http://{HOST}:{PORT}")
    try:httpd.serve_forever()
    except KeyboardInterrupt:pass
if __name__=="__main__":main()
