# Generated by Django 5.0.6 on 2024-07-24 06:17

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("post", "0002_post_picture"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="post",
            name="content",
        ),
    ]
