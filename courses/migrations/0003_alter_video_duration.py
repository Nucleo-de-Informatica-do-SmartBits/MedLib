# Generated by Django 5.1.6 on 2025-03-08 12:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0002_video_uuid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='video',
            name='duration',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]
