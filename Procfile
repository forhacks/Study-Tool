release: python manage.py makemigrations study ; python manage.py migrate
web: gunicorn study-tool.wsgi --log-file -