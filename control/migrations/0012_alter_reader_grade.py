# Generated by Django 5.1.4 on 2025-01-02 05:34

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("control", "0011_remove_reader_photo_remove_reader_slug_reader_uid_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="reader",
            name="grade",
            field=models.CharField(
                choices=[
                    ("10", "Décima"),
                    ("11", "Décima Primeira"),
                    ("12", "Décima Segunda"),
                    ("13", "Décima Terceira"),
                ],
                max_length=3,
                verbose_name="Classe",
            ),
        ),
    ]
