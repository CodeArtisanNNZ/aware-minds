import os
import uuid
os.environ['DATABASE_PATH']='data/test-platform.db'
os.environ['AWARE_MINDS_ENABLE_ACCOUNTS']='1'
from fastapi.testclient import TestClient
from services.api.main import app

def account(client):
    email=str(uuid.uuid4())+'@example.test'
    assert client.post('/api/v1/auth/register',json={'email':email,'password':'correct-horse-battery'}).status_code==200
    return email

def test_app_key_scopes_isolation_and_revocation():
    with TestClient(app) as c:
        account(c)
        slug='test-'+uuid.uuid4().hex[:10]
        assert c.post('/api/v1/developer/apps',json={'name':'Test App','slug':slug}).status_code==200
        assert c.get('/api/v1/developer/apps').status_code==200
        issued=c.post(f'/api/v1/developer/apps/{slug}/keys',json={'scopes':['chat','memory.read']})
        assert issued.status_code==200
        key=issued.json()['key'];key_id=issued.json()['id']
        assert key not in str(c.get(f'/api/v1/developer/apps/{slug}/keys').json())
        assert c.post('/api/v1/memories',json={'app_id':slug,'text':'Private scoped memory'}).status_code==200
        assert c.post(f'/api/v1/integrations/{slug}/memory/search?q=Private',headers={'Authorization':'Bearer '+key}).json()[0]['text']=='Private scoped memory'
        assert c.post('/api/v1/integrations/bujhi/memory/search?q=Private',headers={'Authorization':'Bearer '+key}).status_code==403
        read_only=c.post(f'/api/v1/developer/apps/{slug}/keys',json={'scopes':['memory.read']}).json()['key']
        assert c.post(f'/api/v1/integrations/{slug}/chat',json={'app_id':slug,'message':'Hi'},headers={'Authorization':'Bearer '+read_only}).status_code==403
        assert c.delete(f'/api/v1/developer/apps/{slug}/keys/{key_id}').status_code==200
        assert c.post(f'/api/v1/integrations/{slug}/memory/search?q=Private',headers={'Authorization':'Bearer '+key}).status_code==401
        assert c.get('/api/v1/admin/users').status_code==403
        c.post('/api/v1/auth/logout')
        assert c.get('/api/v1/developer/apps').status_code==401

def test_project_search_and_owner_isolation():
    with TestClient(app) as first, TestClient(app) as second:
        account(first); account(second)
        project=first.post('/api/v1/projects',json={'name':'Research Q4','app_id':'bujhi'}).json()['id']
        assert first.get('/api/v1/projects?app_id=bujhi').json()[0]['id']==project
        assert second.get('/api/v1/projects?app_id=bujhi').json()==[]
        assert second.delete('/api/v1/projects/'+project).status_code==404
        assert len(first.get('/api/v1/search?q=Research&app_id=bujhi').json()['projects'])==1
        assert first.get('/api/v1/search?q=Research&app_id=healthcare-central').json()['projects']==[]
