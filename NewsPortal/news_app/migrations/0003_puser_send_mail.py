# Generated by Django 5.1.2 on 2025-01-03 09:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news_app', '0002_puser_description_puser_subscriptions'),
    ]

    operations = [
        migrations.AddField(
            model_name='puser',
            name='send_mail',
            field=models.BooleanField(default=True),
        ),
    ]
