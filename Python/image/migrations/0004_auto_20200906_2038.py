# Generated by Django 3.1.1 on 2020-09-06 20:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('image', '0003_auto_20200906_2031'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='height',
            field=models.PositiveIntegerField(default=None, null=True),
        ),
        migrations.AlterField(
            model_name='image',
            name='width',
            field=models.PositiveIntegerField(default=None, null=True),
        ),
    ]
