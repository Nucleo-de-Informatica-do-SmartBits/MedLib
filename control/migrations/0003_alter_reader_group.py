# Generated by Django 5.1.4 on 2024-12-30 15:18

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("control", "0002_alter_reader_grade"),
    ]

    operations = [
        migrations.AlterField(
            model_name="reader",
            name="group",
            field=models.CharField(
                choices=[("A", "A"), ("B", "B"), ("C", "C")], max_length=1
            ),
        ),
    ]
