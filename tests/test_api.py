import os
os.environ['DATABASE_PATH']='data/test-aware.db'
os.environ['AWARE_MINDS_ENABLE_ACCOUNTS']='1'
from fastapi.testclient import TestClient
from services.api.main import app

def test_auth_isolation_and_unavailable_model():
    with TestClient(app) as client:
        a=client.post('/api/v1/auth/register',json={'email':'first@example.test','password':'strong-password-1'})
        assert a.status_code in (200,409)
        if a.status_code==409: assert client.post('/api/v1/auth/login',json={'email':'first@example.test','password':'strong-password-1'}).status_code==200
        assert client.post('/api/v1/memories',json={'text':'Only for Bujhi','app_id':'bujhi'}).status_code==200
        assert client.get('/api/v1/memories?app_id=healthcare-central').json()==[]
        assert len(client.get('/api/v1/memories?app_id=bujhi').json())>=1
        assert client.get('/api/v1/admin/overview').status_code==403
        r=client.post('/api/v1/chat',json={'message':'Hello'})
        assert r.status_code in (200,503)
        assert client.post('/api/v1/auth/logout').status_code==200
        assert client.get('/api/v1/apps').status_code==401
