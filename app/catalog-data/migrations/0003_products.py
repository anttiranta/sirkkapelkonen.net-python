from __future__ import unicode_literals

from django.db import migrations, models
from os.path import dirname, abspath
from ..installers.product import ProductDataInstaller

def add_products(apps, schema_editor):
    module_dir = dirname(dirname(abspath(__file__)))

    installer = ProductDataInstaller(apps)
    installer.install([
        module_dir + '/fixtures/product/products_akryyli.csv',
        module_dir + '/fixtures/product/products_akvarelli.csv',
        module_dir + '/fixtures/product/products_oljy.csv',
        module_dir + '/fixtures/product/products_grafiikka.csv',
        module_dir + '/fixtures/product/products_kesakortit.csv',
        module_dir + '/fixtures/product/products_paasiaiskortit.csv',
        module_dir + '/fixtures/product/products_joulukortit.csv',
        module_dir + '/fixtures/product/products_autokortit.csv',
    ])


class Migration(migrations.Migration):

    dependencies = [
        ('www', '0001_initial'),
        ('catalog-data', '0002_categories'),
    ]

    operations = [
        migrations.RunPython(add_products),
    ]
