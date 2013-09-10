python setup.py install
pip install -r example/requirements.txt
python example/example/manage.py collectstatic --noinput --traceback -v 3
python example/example/manage.py syncdb --noinput --traceback -v 3
#python example/example/manage.py migrate --noinput --traceback -v 3