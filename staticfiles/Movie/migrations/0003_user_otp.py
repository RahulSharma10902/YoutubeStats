# Generated by Django 5.1 on 2024-08-26 07:12

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("Movie", "0002_alter_user_username"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="otp",
            field=models.IntegerField(default=None, max_length=4),
        ),
    ]
