# Generated by Django 2.1.2 on 2019-02-28 09:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('picEval', '0002_auto_20190228_0746'),
    ]

    operations = [
        migrations.AlterField(
            model_name='imagetaskinfo',
            name='end_time',
            field=models.TimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='imagetaskinfo',
            name='errorlog',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='imagetaskinfo',
            name='start_time',
            field=models.TimeField(auto_now=True),
        ),
    ]
