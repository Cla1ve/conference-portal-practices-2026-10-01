document.querySelectorAll('.saveStatus').forEach(button=>button.addEventListener('click',async()=>{
 const status_id=Number(document.querySelector(`[data-status="${button.dataset.id}"]`).value);
 try{const r=await api(`/api/admin/requests/${button.dataset.id}`,'PUT',{status_id});
 if(r?.success)message(`Статус заявки №${button.dataset.id} сохранён`,false);else if(r)message(r.message);}catch{message('Не удалось связаться с сервером');}
}));
