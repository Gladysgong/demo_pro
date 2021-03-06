# Generated by Django 2.0.6 on 2019-02-26 09:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    operations = [
        migrations.CreateModel(
            name='ImageTaskInfo',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('status', models.IntegerField(default=0)),
                ('env_type', models.IntegerField(default=0)),
                ('start_time', models.TimeField()),
                ('end_time', models.TimeField()),
                ('testtag', models.CharField(default='', max_length=50)),
                ('errorlog', models.TextField()),
                ('pid', models.CharField(default='', max_length=50)),
                ('sum_num', models.IntegerField(default=0)),
                ('finished', models.IntegerField(default=0)),
                ('failed', models.IntegerField(default=0)),
                ('img_diff_count', models.IntegerField(default=0)),
                ('text_diff_count', models.IntegerField(default=0)),
                ('text_base_count', models.IntegerField(default=0)),
                ('langs', models.CharField(default='', max_length=50)),
                ('svIP', models.CharField(default='', max_length=50)),
                ('svUser', models.CharField(default='', max_length=100)),
                ('svPass', models.CharField(default='', max_length=100)),
                ('svPath', models.CharField(default='', max_length=500)),
                ('sourceIP', models.CharField(default='', max_length=50)),
                ('sourceUser', models.CharField(default='', max_length=100)),
                ('sourcePass', models.CharField(default='', max_length=100)),
                ('sourcePath', models.CharField(default='', max_length=500)),
            ],
        ),
        migrations.CreateModel(
            name='ResultInfo',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('testImg', models.CharField(default='', max_length=500)),
                ('basepath', models.CharField(default='', max_length=500)),
                ('testpath', models.CharField(default='', max_length=500)),
                ('result', models.TextField()),
                ('rankInfo', models.IntegerField(default=0)),
                ('test_status', models.IntegerField(default=0)),
                ('base_status', models.IntegerField(default=0)),
                ('taskid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='picEval.ImageTaskInfo')),
            ],
        ),
    ]
