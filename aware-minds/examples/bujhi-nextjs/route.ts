// Place in app/api/aware-chat/route.ts in your Next.js project.
// Authenticate the student on your server. This prototype key is a shared service account.
export async function POST(request:Request){
  const {message}=await request.json();
  if(typeof message!=='string'||!message.trim())return Response.json({error:'Message required'},{status:400});
  const apiKey=process.env.AWARE_MINDS_KEY;
  if(!apiKey)return Response.json({error:'AI unavailable'},{status:503});
  try{
    const response=await fetch(`${process.env.AWARE_MINDS_URL||'http://127.0.0.1:8000'}/api/v1/integrations/bujhi/chat`,{
      method:'POST',headers:{Authorization:`Bearer ${apiKey}`,'Content-Type':'application/json'},
      body:JSON.stringify({app_id:'bujhi',message})
    });
    return Response.json(await response.json(),{status:response.status});
  }catch{return Response.json({error:'AI unavailable'},{status:502})}
}
