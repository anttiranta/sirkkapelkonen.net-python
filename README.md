Sirkka Pelkonen's Homepage (Python version)
===========================================

General
-------

Python/Django version of sirkkapelkonen.net (homepage of artist Sirkka Pelkonen). 

Most of the code is from 2016, although Django and readme I updated before pushing the code to Github. 
This site was never used in production, it's simply just a hobby project of mine. 

![Image of sirkkapelkonen.net](https://raw.githubusercontent.com/anttiranta/sirkkapelkonen.net/master/screenshots/web_sirkkap.jpg)


Local development
-----------------

### Development in Windows

* Download and install [Python
  3.5.x](https://www.python.org/ftp/python/3.5.3/python-3.5.3.exe).  For this
  guide, I assume Python is installed in `C:\Python35`.
* Download the Pip (Python package installer) bootstrap script
  [get-pip.py](https://bootstrap.pypa.io/get-pip.py).
* In the command prompt, run `C:\Python35\python.exe get-pip.py` to install
  `pip`.
* In the command prompt, run `C:\Python35\scripts\pip install virtualenv` to
  install `virtualenv`.

### Development in Ubuntu

Python 3 is preinstalled in Ubuntu. Virtualenv and pip necessarily aren't, so:

* `sudo apt-get install python-virtualenv python-pip`

### Creating and activating a virtualenv

Go to the project root directory and run:

Windows:

```
c:\location_of_project>c:\Python35\scripts\virtualenv --system-site-packages venv
c:\location_of_project>venv\Scripts\activate
```

Ubuntu:

```
virtualenv -p /usr/bin/python3 --system-site-packages venv
source venv/bin/activate
```

### Starting the project

After activating the virtualenv do the following

```
cd app
pip install -r requirements.txt
python manage.py migrate --noinput
python manage.py runserver
```

Now the website should be visible in the browser at
[`http://127.0.0.1:8000/`](http://127.0.0.1:8000/).