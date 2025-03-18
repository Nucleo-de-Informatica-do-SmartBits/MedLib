# Generated by Django 5.1.6 on 2025-03-13 15:17

import django.core.validators
import django.db.models.deletion
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('control', '0002_reader_photo'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='reader',
            name='course',
            field=models.CharField(blank=True, choices=[('Informática', 'Informática'), ('Eletrónica', 'Eletrónica')], max_length=30, null=True, verbose_name='Curso'),
        ),
        migrations.AlterField(
            model_name='reader',
            name='grade',
            field=models.CharField(blank=True, choices=[('10', 'Décima'), ('11', 'Décima Primeira'), ('12', 'Décima Segunda'), ('13', 'Décima Terceira')], max_length=3, null=True, verbose_name='Classe'),
        ),
        migrations.AlterField(
            model_name='reader',
            name='group',
            field=models.CharField(blank=True, choices=[('A', 'Turma A'), ('B', 'Turma B'), ('C', 'Turma C'), ('D', 'Turma D')], max_length=1, null=True, verbose_name='Turma'),
        ),
        migrations.AlterField(
            model_name='reader',
            name='process_number',
            field=models.IntegerField(blank=True, null=True, unique=True, validators=[django.core.validators.MinValueValidator(1)], verbose_name='Número de Processo'),
        ),
        migrations.AlterField(
            model_name='reader',
            name='uid',
            field=models.UUIDField(blank=True, default=uuid.uuid4, editable=False, null=True, unique=True, verbose_name='Identificador Universal'),
        ),
        migrations.AlterField(
            model_name='reader',
            name='user',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='reader', to=settings.AUTH_USER_MODEL),
        ),
    ]
