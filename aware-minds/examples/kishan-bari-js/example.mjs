// Node.js server example, never import into a browser bundle.
const response=await fetch(`${process.env.AWARE_MINDS_URL||'http://127.0.0.1:8000'}/api/v1/integrations/kishan-bari/chat`,{
 method:'POST',headers:{Authorization:`Bearer ${process.env.AWARE_MINDS_KEY}`,'Content-Type':'application/json'},
 body:JSON.stringify({app_id:'kishan-bari',message:'Explain soil pH in Bangla'})
});
if(!response.ok)throw new Error(`Aware Minds returned ${response.status}`);
console.log((await response.json()).message);
