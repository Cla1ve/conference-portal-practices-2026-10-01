async function api(url,method='GET',data){
  const headers={'X-CSRF-Token':document.querySelector('meta[name="csrf-token"]').content};
  if(data!==undefined)headers['Content-Type']='application/json';
  const response=await fetch(url,{method,headers,body:data===undefined?undefined:JSON.stringify(data)});
  const result=await response.json();
  if(response.status===401&&url!=='/api/auth/login'){location.href='/api/auth/login';return null;}
  return result;
}
function message(text,error=true){const el=document.getElementById('message');el.textContent=text;el.className=error?'error':'success';}
document.getElementById('logout')?.addEventListener('click',async()=>{
  try{const r=await api('/api/auth/logout','POST',{});if(r?.success)location.href=r.redirect;else if(r)message(r.message);}catch{message('Не удалось связаться с сервером');}
});
