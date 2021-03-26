release: sh -c 'python manage.py migrate'
web: sh -c 'gunicorn citra.wsgi --log-file -'