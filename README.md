# Django Image Upload
## Описание
Веб приложение с возможностью загрузки изображений и изменению их размера. 
## Стек
Python, Django, Pillow
## Инструкция по запуску
Вариант №1 (необходимо чтобы на локальном компьютере был установлен Python3):
1. Склонируйте репозиторий на свой локальный компьютер.
2. В корневой директории проекта установите виртуальное окружение используя команду `python3 -m venv venv`.
3. Установите необходимые библиотеки используя команду `pip install -r requirements.txt`.
4. Выполните миграции командой `python manage.py migrate`.
5. Запустите локальный сервер командой `python manage.py runserver`.
6. Приложение будет доступно в браузере по адресу http://127.0.0.1:8000/.

Вариант №2 (необходимо чтобы на локальном компьютере был установлен Docker):
1. Склонируйте репозиторий на свой локальный компьютер.
2. В корневой директории проекта создайте образ командой `docker build -t image-upload .`
3. Запустите контейнер командой `docker run -it -p 8000:8000 image-upload`.
4. Приложение будет доступно в браузере по адресу http://localhost:8000/.
