release: sh -c 'python manage.py migrate'
web: sh -c 'cd doc && gunicorn citra.wsgi --log-file -'