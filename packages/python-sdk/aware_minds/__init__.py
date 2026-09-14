"""Server-side Aware Minds integration. Keep keys off public clients."""
import json
import urllib.request
import urllib.error

class AwareMinds:
    def __init__(self,base_url:str,app_id:str,api_key:str):
        self.base_url=base_url.rstrip('/')
        self.app_id=app_id
        self.api_key=api_key

    def health(self):
        with urllib.request.urlopen(self.base_url+'/health',timeout=5) as response:
            return json.load(response)

    def chat(self,message:str,conversation_id:str|None=None):
        request=urllib.request.Request(
            f'{self.base_url}/api/v1/integrations/{self.app_id}/chat',
            data=json.dumps({'app_id':self.app_id,'message':message,'conversation_id':conversation_id}).encode(),
            headers={'Authorization':'Bearer '+self.api_key,'Content-Type':'application/json'},
            method='POST')
        with urllib.request.urlopen(request,timeout=120) as response:
            return json.load(response)
