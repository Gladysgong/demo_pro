# Generated by Django 2.0.1 on 2018-08-10 06:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rbac', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userinfo',
            name='email',
        ),
        migrations.RemoveField(
            model_name='userinfo',
            name='nickname',
        ),
        migrations.RemoveField(
            model_name='userinfo',
            name='password',
        ),
    ]
