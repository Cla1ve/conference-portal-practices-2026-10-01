document.getElementById('loginForm').addEventListener('submit',async(e)=>{
 e.preventDefault();try{const r=await api('/api/auth/login','POST',Object.fromEntries(new FormData(e.target)));
 if(r.success)location.href=r.redirect;else message(r.message);}catch{message('Не удалось связаться с сервером');}
});
