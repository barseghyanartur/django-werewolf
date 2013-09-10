wget -O django_werewolf_example_app.tar.gz https://github.com/barseghyanartur/django-werewolf/archive/stable.tar.gz
mkdir django_werewolf_example_app/
tar -xvf django_werewolf_example_app.tar.gz -C django_werewolf_example_app
cd django_werewolf_example_app/django-werewolf-stable/example/example/
pip install Django
pip install -r ../requirements.txt
mkdir ../media/
mkdir ../media/static/
mkdir ../static/
mkdir ../db/
cp local_settings.example local_settings.py
./manage.py syncdb --noinput
./manage.py collectstatic --noinput
./manage.py runserver
