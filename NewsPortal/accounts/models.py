from django.db import models
from news_app.models import Puser


class Subscriptions(models.Model):
    follower = models.ForeignKey(Puser, on_delete=models.CASCADE, related_name='followers')
    sub = models.ForeignKey(Puser, on_delete=models.CASCADE, related_name='subs')

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['follower', 'sub'], name='unique_follower_sub')
        ]