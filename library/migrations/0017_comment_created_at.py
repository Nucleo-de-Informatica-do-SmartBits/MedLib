# Generated by Django 5.1.6 on 2025-03-02 17:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0016_remove_comment_dislikes_remove_comment_likes'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
