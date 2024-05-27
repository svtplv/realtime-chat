# realtime-chat
## Описание:

Чат в реальном времени на основе вебсокетов с помощью django channels и htmx. На данный момент есть общий чат и приватный между двумя пользователями.


### Стек технологий:
* Python 3.12
* Django 5
* Django Channels
* Redis
* HTMX
* Tailwind

### Установка:

1. Клонировать репозиторий и перейти в него в командной строке:
```
git@github.com:svtplv/realtime-chat.git
```

2. Cоздать и активировать виртуальное окружение:
* Linux/macOS:
```
python3 -m venv venv
source venv/bin/activate
```
* Windows:
```
python -m venv venv
source env/scripts/activate
```

3. Установить зависимости из файла requirements.txt:
```
pip install -r requirements.txt
```

4. Запустить redis:

```
redis-server.exe
```

5. Cоздать миграции:

```
python manage.py makemigrations
```

6. Применить миграции:

```
python manage.py migrate
```

7. Запустить проект:
``` 
python manage.py runserver
```
