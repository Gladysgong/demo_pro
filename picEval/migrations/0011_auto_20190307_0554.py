# Generated by Django 2.1.2 on 2019-03-07 05:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('picEval', '0010_resultinfo_filename'),
    ]

    operations = [
        migrations.AlterField(
            model_name='imagetaskinfo',
            name='errorlog',
            field=models.TextField(default=''),
        ),
    ]