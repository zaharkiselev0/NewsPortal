# Generated by Django 5.1.2 on 2025-01-12 23:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
        ('news_app', '0003_puser_send_mail'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='subscriptions',
            constraint=models.UniqueConstraint(fields=('follower', 'sub'), name='unique_follower_sub'),
        ),
    ]
