# Generated by Django 5.1.6 on 2025-03-07 20:20

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0010_course_stars'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='content',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='comment',
            name='video',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='courses.video'),
        ),
        migrations.AlterField(
            model_name='course',
            name='name',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='course',
            name='slug',
            field=models.SlugField(blank=True, editable=False, null=True, unique=True),
        ),
        migrations.RemoveField(
            model_name='course',
            name='stars',
        ),
        migrations.AlterField(
            model_name='video',
            name='course',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='courses.course'),
        ),
        migrations.AlterField(
            model_name='video',
            name='slug',
            field=models.SlugField(blank=True, editable=False, null=True),
        ),
        migrations.AlterField(
            model_name='video',
            name='title',
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
        migrations.AddField(
            model_name='course',
            name='stars',
            field=models.ManyToManyField(blank=True, null=True, related_name='courses_with_user_stars', to=settings.AUTH_USER_MODEL),
        ),
    ]
