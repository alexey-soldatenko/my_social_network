# my_social_network
Данный проект представляет собой простую социальную сеть.
В ходе разработки использовались python3.5 и django1.8
После того, как вы скачали/клонировали проект, он запускается также как и любое ваше django-приложение на отладочном сервисе.

python3 manage.py runserver

Главная страница предполагает вашу регистрацию, с подтверждением эл.почты. Однако в базе данных уже есть несколько 
зарегистрированных пользователей, их адреса '/person/id_1000', '/person/id_1001', '/person/id_1002'.

Если вы удаляете базу данных, перед запуском выполните python3 manage.py syncdb или python3 manage.py createsuperuser. Создайте 
администратора, среди вводимых данных будет person_id - это значение как раз и соответствует 'person/id_<b>person_id</b>' адреса 
страницы пользователя. Дальнейшие значения person_id других зарегистрированных пользователей, будут расчитаны как значение 
person_id последнего зарегистрированного пользователя +1.
