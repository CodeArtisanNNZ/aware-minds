const CACHE='aware-minds-shell-v1';
self.addEventListener('install',event=>{event.waitUntil(caches.open(CACHE).then(cache=>cache.addAll(['/','/icon.svg','/manifest.webmanifest'])));self.skipWaiting()});
self.addEventListener('activate',event=>{event.waitUntil(caches.keys().then(keys=>Promise.all(keys.filter(k=>k!==CACHE).map(k=>caches.delete(k)))));self.clients.claim()});
self.addEventListener('fetch',event=>{const request=event.request;if(request.method!=='GET'||request.url.includes('/api/')||request.url.includes('/health'))return;if(request.mode==='navigate'){event.respondWith(fetch(request).catch(()=>caches.match('/')));return}event.respondWith(fetch(request).catch(()=>caches.match(request)))});
