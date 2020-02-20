from __future__ import unicode_literals

from django.db import migrations, models
from os.path import dirname, abspath
from ..installers.category import CategoryDataInstaller

def add_categories(apps, schema_editor):
    module_dir = dirname(dirname(abspath(__file__)))

    installer = CategoryDataInstaller(apps)
    installer.install([module_dir + '/fixtures/categories.csv'])


class Migration(migrations.Migration):

    dependencies = [
        ('www', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(add_categories),
    ]
