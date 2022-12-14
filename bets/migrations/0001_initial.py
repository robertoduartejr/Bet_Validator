# Generated by Django 4.1.1 on 2022-09-20 14:53

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Jogos',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mandante', models.CharField(max_length=100)),
                ('visitante', models.CharField(max_length=100)),
                ('liga', models.CharField(max_length=100)),
                ('goals_last5', models.IntegerField(default=0)),
                ('approved', models.BooleanField(default=False)),
                ('approve_details', models.CharField(max_length=300)),
                ('game_date', models.DateField(default=datetime.date(2022, 9, 20))),
            ],
        ),
    ]
