/** Server-side SDK. Never bundle an application API key into browser JavaScript. */
export type ChatRequest={message:string;conversationId?:string};
export type ChatResponse={conversation_id:string;message:string;provider:string;model:string;citations:{document_id:string;filename:string}[]};
export class AwareMinds {
  constructor(private config:{baseUrl:string;appId:string;apiKey:string}){}
  private async request<T>(path:string,body:unknown):Promise<T>{
    const response=await fetch(this.config.baseUrl.replace(/\/$/,'')+'/api/v1/integrations/'+encodeURIComponent(this.config.appId)+path,{method:'POST',headers:{'Authorization':'Bearer '+this.config.apiKey,'Content-Type':'application/json'},body:JSON.stringify(body)});
    if(!response.ok)throw new Error(`Aware Minds ${response.status}: ${await response.text()}`);
    return response.json() as Promise<T>;
  }
  chat(input:ChatRequest){return this.request<ChatResponse>('/chat',{app_id:this.config.appId,message:input.message,conversation_id:input.conversationId??null});}
  searchMemory(query:string){return this.request<{id:string;text:string}[]>('/memory/search?q='+encodeURIComponent(query),{});}
}
