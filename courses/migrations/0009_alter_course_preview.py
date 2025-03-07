# Generated by Django 5.1.4 on 2025-03-07 20:06

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("courses", "0008_remove_course_categories_course_category"),
    ]

    operations = [
        migrations.AlterField(
            model_name="course",
            name="preview",
            field=models.FileField(
                blank=True,
                null=True,
                upload_to="course-preview/",
                verbose_name="preview",
            ),
        ),
    ]
