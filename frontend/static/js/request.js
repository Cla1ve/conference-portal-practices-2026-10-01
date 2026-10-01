document.getElementById('requestForm')?.addEventListener('submit',async(e)=>{
 e.preventDefault();const data=Object.fromEntries(new FormData(e.target));
 if(data.name.trim().length<2)return message('Введите название помещения');
 if(!/^\d{4}-\d{2}-\d{2}$/.test(data.date)||!/^\d{2}:\d{2}$/.test(data.start_time))return message('Дата в формате ГГГГ-ММ-ДД, время ЧЧ:ММ');
 try{const r=await api('/api/requests','POST',data);if(r?.success)location.href=r.redirect;else if(r)message(r.message);}catch{message('Не удалось связаться с сервером');}
});
document.querySelectorAll('.reviewForm').forEach(form=>form.addEventListener('submit',async(e)=>{
 e.preventDefault();const data=Object.fromEntries(new FormData(form));data.rating=Number(data.rating);
 try{const r=await api(`/api/requests/${form.dataset.id}/review`,'POST',data);if(r?.success)location.reload();else if(r)message(r.message);}catch{message('Не удалось связаться с сервером');}
}));
