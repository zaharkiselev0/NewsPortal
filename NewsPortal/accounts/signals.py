from allauth.account.signals import user_signed_up
from django.db.models.signals import post_save
from django.dispatch import receiver

from django.contrib.auth.models import User
from django.core.mail import send_mail

from news_app.models import Post, Puser
from .tasks import mail_signed_up_task, post_created_task


@receiver(user_signed_up)
def mail_signed_up(request, user, **kwargs):
    mail_signed_up_task.delay(user.pk)


@receiver(post_save, sender=Post)
def post_created(instance, created, **kwargs):
    if created:
        post_created_task.delay(instance.pk)

