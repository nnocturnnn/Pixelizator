# Generated by Django 3.1.1 on 2020-09-07 18:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('image', '0006_auto_20200907_1848'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='url',
            field=models.URLField(blank=True, null=True),
        ),
    ]