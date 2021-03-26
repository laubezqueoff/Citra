release: sh -c 'cd Citra && python manage.py migrate'
web: sh -c 'cd doc && gunicorn citra.wsgi --log-file -'