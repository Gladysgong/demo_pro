# Generated by Django 2.1.2 on 2019-03-01 10:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('picEval', '0006_auto_20190228_1103'),
    ]

    operations = [
        migrations.RenameField(
            model_name='imagetaskinfo',
            old_name='base_ip',
            new_name='base_imgip',
        ),
        migrations.RenameField(
            model_name='imagetaskinfo',
            old_name='test_ip',
            new_name='base_ocrip',
        ),
        migrations.AddField(
            model_name='imagetaskinfo',
            name='test_imgip',
            field=models.CharField(default='', max_length=50),
        ),
        migrations.AddField(
            model_name='imagetaskinfo',
            name='test_ocrip',
            field=models.CharField(default='', max_length=50),
        ),
    ]
