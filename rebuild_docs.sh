./uninstall.sh
./install.sh
rm docs/*.rst
rm -rf builddocs/
sphinx-apidoc src/dash --full -o docs -H 'django-werewolf' -A 'Artur Barseghyan <artur.barseghyan@gmail.com>' -f -d 20
cp docs/conf.py.distrib docs/conf.py