# Generated by Django 2.2.4 on 2020-10-20 05:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pythonexamApp', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='firstname',
            new_name='name',
        ),
        migrations.RenameField(
            model_name='user',
            old_name='lastname',
            new_name='username',
        ),
    ]
