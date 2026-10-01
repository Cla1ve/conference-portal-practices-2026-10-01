import re
from datetime import date, datetime


class Validator:
    @staticmethod
    def registration(user):
        checks = [
            (user.login, r'[A-Za-z0-9]{6,50}', 'Логин: от 6 до 50 символов, латиница и цифры'),
            (user.fio, r'[А-Яа-яЁё ]{2,150}', 'ФИО: кириллица и пробелы'),
            (user.email, r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}', 'Некорректный email'),
            (user.phone, r'8\([0-9]{3}\)[0-9]{3}-[0-9]{2}-[0-9]{2}', 'Телефон в формате 8(XXX)XXX-XX-XX'),
        ]
        for value, pattern, message in checks:
            if not isinstance(value,str) or not re.fullmatch(pattern,value):
                return False,message
        if len(user.email)>100:
            return False,'Email слишком длинный'
        if not isinstance(user.password,str) or not 8 <= len(user.password) <= 128:
            return False,'Пароль должен содержать от 8 до 128 символов'
        return True,''

    @staticmethod
    def event(event):
        if not isinstance(event.name,str) or not 2<=len(event.name.strip())<=200:
            return False,'Введите название помещения от 2 до 200 символов'
        if re.search(r'[\x00-\x1f\x7f]',event.name):
            return False,'Название содержит недопустимые символы'
        if event.place not in ('Аудитория','Коворкинг','Кинозал'):
            return False,'Выберите тип помещения'
        try:
            if not isinstance(event.date,str) or not re.fullmatch(r'\d{4}-\d{2}-\d{2}',event.date):
                raise ValueError()
            if not isinstance(event.start_time,str) or not re.fullmatch(r'\d{2}:\d{2}',event.start_time):
                raise ValueError()
            when=datetime.fromisoformat(event.date+'T'+event.start_time)
            if when < datetime.now():
                return False,'Выберите будущие дату и время'
        except (ValueError,TypeError):
            return False,'Дата в формате ГГГГ-ММ-ДД, время ЧЧ:ММ'
        return True,''
