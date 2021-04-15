release: sh -c 'python manage.py migrate'
web: sh -c 'gunicorn Citra.wsgi --log-file -'