"""Model transport adapters. Credentials are server-side environment variables only."""
import json
import os
import urllib.error
import urllib.request


def configuration():
    provider = os.getenv('AI_PROVIDER', 'ollama').lower()
    if provider == 'hosted':
        base = os.getenv('HOSTED_AI_BASE_URL', '').rstrip('/')
        key = os.getenv('HOSTED_AI_API_KEY', '')
        model = os.getenv('HOSTED_AI_MODEL', '')
        if not base.startswith('https://') or not key or not model:
            return None
        return provider, model, base, key
    if provider != 'ollama':
        return None
    return provider, os.getenv('OLLAMA_MODEL', ''), os.getenv('OLLAMA_BASE_URL', 'http://127.0.0.1:11434').rstrip('/'), ''


def available_models():
    config = configuration()
    if not config:
        return []
    provider, model, base, _ = config
    if provider == 'hosted':
        return [model]
    try:
        with urllib.request.urlopen(base + '/api/tags', timeout=2) as response:
            return [item['name'] for item in json.load(response).get('models', [])]
    except (urllib.error.URLError, TimeoutError, ValueError):
        return []


def _request(model, messages, streaming):
    config = configuration()
    if not config:
        raise ValueError('Model provider not configured')
    provider, _, base, key = config
    if provider == 'hosted':
        url = base + '/chat/completions'
        headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + key}
    else:
        url = base + '/api/chat'
        headers = {'Content-Type': 'application/json'}
    payload = {'model': model, 'messages': messages, 'stream': streaming}
    return urllib.request.urlopen(urllib.request.Request(url, data=json.dumps(payload).encode(), headers=headers), timeout=90)


def complete(model, messages):
    with _request(model, messages, False) as response:
        packet = json.load(response)
    if configuration()[0] == 'hosted':
        return packet['choices'][0]['message']['content']
    return packet['message']['content']


def deltas(model, messages):
    with _request(model, messages, True) as response:
        if configuration()[0] == 'ollama':
            for line in response:
                if line.strip():
                    chunk = json.loads(line).get('message', {}).get('content', '')
                    if chunk:
                        yield chunk
        else:
            for line in response:
                if not line.startswith(b'data: '):
                    continue
                data = line[6:].strip()
                if data == b'[DONE]':
                    break
                chunk = json.loads(data)['choices'][0].get('delta', {}).get('content', '')
                if chunk:
                    yield chunk
