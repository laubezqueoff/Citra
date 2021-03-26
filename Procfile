release: sh -c 'cd Citra && python manage.py migrate'
web: sh -c 'cd doc && cd Citra && gunicorn citra.wsgi --log-file -'