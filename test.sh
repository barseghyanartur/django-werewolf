reset
pip install -r example/requirements.txt

./uninstall.sh
./install.sh

# Django tests
python example/example/manage.py test werewolf --traceback -v 3