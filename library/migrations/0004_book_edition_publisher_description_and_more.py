# Generated by Django 5.1.4 on 2025-01-16 19:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0003_alter_book_authors_alter_book_categories'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='edition',
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name='Edição'),
        ),
        migrations.AddField(
            model_name='publisher',
            name='description',
            field=models.TextField(blank=True, max_length=150, null=True, verbose_name='Descrição'),
        ),
        migrations.AlterField(
            model_name='publisher',
            name='address',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Endereço'),
        ),
    ]
