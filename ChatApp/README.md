
Чат с использованием Django REST Framework
Стиль с Materialize Framework

-----------------------------
ИНСТРУКЦИЯ ПО УСТАНОВКЕ
-----------------------------



Установка приложения
______________________________________________________________________________________

Для отображения статуса пользователей (в сети\не в сети) необходимо устрановить memcached 



Установка виртуального окружения
--------------
pip install virtualenv
--------------


В директории проекта создать virtualenv venv
--------------------
virtualenv venv
-------------------


Активировать(выполнить, в директории \venv\Scripts\)

----------------------------
activate
-------------------------


Установка requirements
---------------------------
pip install -r requirements.txt
---------------------------

Выполнить migrations к базе данных(из директории проекта)

--------------------------------
python manage.py makemigrations
python manage.py makemigrations chat
python manage.py migrate
------------------------------

Создать пользователя для возможности управления
(Символы пароля просто не отображаются)

---------------------
python manage.py createsuperuser
---------------------


Запустить сервер

---------------------
python manage.py runserver
---------------------
