import os
from setuptools import setup, find_packages

try:
    readme = open(os.path.join(os.path.dirname(__file__), 'readme.rst')).read()
except:
    readme = ''

version = '0.1'

setup(
    name='django-werewolf',
    version=version,
    description=("Item publishing workflow for Django."),
    long_description=readme,
    classifiers=[
        'Programming Language :: Python',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
    ],
    keywords='workflow, publishing',
    author='Artur Barseghyan',
    author_email='artur.barseghyan@gmail.com',
    url='https://bitbucket.org/barseghyanartur/django-werewolf',
    package_dir={'':'src'},
    packages=find_packages(where='./src'),
    license='GPL 2.0/LGPL 2.1',
    install_requires=['django-reversion==1.6.5']
)
