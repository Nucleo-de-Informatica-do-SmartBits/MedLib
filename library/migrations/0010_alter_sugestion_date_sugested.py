# Generated by Django 5.1.4 on 2025-01-17 22:02

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0009_alter_sugestion_date_sugested'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sugestion',
            name='date_sugested',
            field=models.DateTimeField(default=datetime.datetime(2025, 1, 17, 22, 2, 49, 508427, tzinfo=datetime.timezone.utc), verbose_name='data'),
        ),
    ]
