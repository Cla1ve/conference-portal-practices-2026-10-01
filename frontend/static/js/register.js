document.getElementById('registerForm').addEventListener('submit',async(e)=>{
 e.preventDefault();const data=Object.fromEntries(new FormData(e.target));
 for(const key of ['login','fio','email','phone'])data[key]=data[key].trim();
 if(!/^[A-Za-z0-9]{6,50}$/.test(data.login))return message('Логин: от 6 до 50 символов, латиница и цифры');
 if(data.password.length<8||data.password.length>128)return message('Пароль должен содержать от 8 до 128 символов');
 if(!/^[А-Яа-яЁё ]{2,150}$/.test(data.fio))return message('ФИО: кириллица и пробелы');
 if(!/^8\([0-9]{3}\)[0-9]{3}-[0-9]{2}-[0-9]{2}$/.test(data.phone))return message('Телефон в формате 8(XXX)XXX-XX-XX');
 if(!/^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$/.test(data.email))return message('Некорректный email');
 try{const r=await api('/api/auth/register','POST',data);if(r.success){message(r.message,false);e.target.reset();}else message(r.message);}catch{message('Не удалось связаться с сервером');}
});
