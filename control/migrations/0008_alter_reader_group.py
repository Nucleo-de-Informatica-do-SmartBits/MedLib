# Generated by Django 5.1.4 on 2024-12-31 20:16

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("control", "0007_alter_reader_group_alter_reader_slug"),
    ]

    operations = [
        migrations.AlterField(
            model_name="reader",
            name="group",
            field=models.CharField(
                choices=[
                    ("C", "Turma C"),
                    ("B", "Turma B"),
                    ("A", "Turma A"),
                    ("D", "Turma D"),
                ],
                max_length=3,
                verbose_name="Turma",
            ),
        ),
    ]
