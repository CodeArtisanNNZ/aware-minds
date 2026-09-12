import os
from aware_minds import AwareMinds

client=AwareMinds(os.getenv('AWARE_MINDS_URL','http://127.0.0.1:8000'),'kalra',os.environ['AWARE_MINDS_KEY'])
print(client.chat('Help me plan my day')['message'])
