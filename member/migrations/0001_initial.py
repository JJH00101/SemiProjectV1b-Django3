# Generated by Django 3.2.13 on 2022-06-23 03:06

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Member',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('userid', models.CharField(max_length=18, unique=True)),
                ('passwd', models.CharField(max_length=18)),
                ('name', models.CharField(max_length=5)),
                ('email', models.CharField(max_length=100)),
                ('regdate', models.DateTimeField(default=datetime.datetime.now)),
            ],
            options={
                'db_table': 'member',
                'ordering': ['-regdate'],
            },
        ),
    ]
