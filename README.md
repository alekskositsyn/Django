# Интернет-магазин "MIXER"

## О проекте:

<br>Проект разработан на фреймворке Django.</br>
<br>В проекте есть своя собственная административная панель, в которой можно управять пользователями
и товарами.</br>

### Возможности пользователя:
<li>Регистрация с отправкой письма подтверждения почты пользователя</li>
<li>Создание профиля и редактирование его</li>
<li>Корзина товаров</li>
<li>Список заказов и редактирование заказов</li>



## Установка 
Для запуска необходимо скачать проект через github или скачать архив и распаковать его.
Создать виртальное окружение в папке проекта:

```bash 
python3 -m venv env
```
Активировать окружение:
```bash 
source env/bin/activate
```
Скачать зависимости проекта из requirements.txt:
```bash
pip install -r requirements.txt
```
Для запуска проекта необходимо ввести:
```bash
python manage.py runserver
```
И перейти в браузере по ссылке:
`http://127.0.0.1:8000/`

<br>Для того чтобы попать в аккаунт администратора:</br>
Логин:
`django`
Пароль:
`geekbrains`

