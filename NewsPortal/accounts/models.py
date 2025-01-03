from django.db import models
from news_app.models import Puser


class Subscriptions(models.Model):
    follower = models.ForeignKey(Puser, on_delete=models.CASCADE, related_name='followers')
    sub = models.ForeignKey(Puser, on_delete=models.CASCADE, related_name='subs')
