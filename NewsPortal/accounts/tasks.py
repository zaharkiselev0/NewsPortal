from celery import shared_task
from celery.exceptions import SoftTimeLimitExceeded

from news_app.models import User, Post
from django.core.mail import send_mail

from datetime import datetime, timedelta

import time


@shared_task(soft_time_limit=10, time_limit=15)
def mail_signed_up_task(user_id):
    try:
        user = User.objects.get(pk=user_id)
        subject = 'Вы успешно зарегестрировались на сайте!'
        message = f'Добро пожаловать, {user.username}!'
        send_mail(subject, message, 'none', [user.email])
    except SoftTimeLimitExceeded:
        print('Письмо при регистрации не отправлено')


# Работает, но адекватность под вопросом
text_subject_numtask_dict = dict()
@shared_task(soft_time_limit=10, time_limit=15)
def post_created_mail_user_task(user_id, post_id):
    text_subject_numtask = text_subject_numtask_dict[post_id]
    subject = text_subject_numtask[0]
    text_content = text_subject_numtask[1]
    text_subject_numtask[2] -= 1
    user = User.objects.get(pk=user_id)
    send_mail(subject, text_content, 'none', [user.email])
    if not text_subject_numtask[2]:
        text_subject_numtask_dict.pop(post_id)


@shared_task(soft_time_limit=10, time_limit=15)
def post_created_task(post_id):
    post = Post.objects.get(pk=post_id)
    users_id = User.objects.filter(
        puser__followers__sub=post.puser
    ).values_list('pk', flat=True)
    subject = f'Новая статья от {post.puser.user.username}'
    text = (
        f'Пост: {post.title}\n'
        f'Ссылка на пост: http://127.0.0.1:8000{post.get_absolute_url()}'
    )
    text_subject_numtask_dict[post_id] = [subject, text, len(users_id)]
    for uid in users_id:
        post_created_mail_user_task.delay(uid, post_id)


weekly_mail_text_message = ''
@shared_task(soft_time_limit=10, time_limit=15)
def weekly_mail_user_task(user_id):
    user = User.objects.get(pk=user_id)
    send_mail('Новые посты на localhost-е!', weekly_mail_text_message, 'none', [user.email])


@shared_task(soft_time_limit=10, time_limit=15)
def weekly_mail_task():
    global weekly_mail_text_message
    tm = datetime.now() - timedelta(weeks=1)
    posts = Post.objects.filter(date__gt=tm)
    weekly_mail_text_message = '\n'.join([f'Пост: {post.title}\n'
                      f'Ссылка на пост: http://127.0.0.1:8000{post.get_absolute_url()}' for post in posts])

    users_id = User.objects.filter(puser__send_mail=True).values_list('pk', flat=True)
    for uid in users_id:
        weekly_mail_user_task.delay(uid)
