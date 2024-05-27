# Generated by Django 5.0.6 on 2024-05-26 03:45

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("chat", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="groupmessage",
            options={"ordering": ["created"]},
        ),
        migrations.AddField(
            model_name="chatgroup",
            name="users_online",
            field=models.ManyToManyField(
                blank=True, related_name="online_in_groups", to=settings.AUTH_USER_MODEL
            ),
        ),
    ]