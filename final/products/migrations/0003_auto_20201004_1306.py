# Generated by Django 3.1.1 on 2020-10-04 11:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_auto_20201004_1251'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='vat',
            field=models.IntegerField(default=23),
        ),
    ]
