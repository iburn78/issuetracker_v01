# Generated by Django 2.2.3 on 2019-12-01 20:48

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0010_auto_20191201_1956'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='pub_date',
            field=models.DateTimeField(default=datetime.datetime(2019, 12, 1, 20, 48, 51, 842703), verbose_name='date published'),
        ),
    ]
