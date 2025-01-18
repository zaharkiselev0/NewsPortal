from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum
from django.urls import reverse
from django.core.cache import cache

from django.utils.translation import gettext as _
from django.utils.translation import pgettext_lazy # импортируем «ленивый» геттекст с подсказкой


class Puser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    rating = models.IntegerField(default=0)
    subscriptions = models.ManyToManyField('Puser', through='accounts.Subscriptions')
    description = models.TextField(default='')
    send_mail = models.BooleanField(default=True)

    def update_rating(self):
        rating = self.comment_set.exclude(post__author__puser=self).aggregate(Sum('rating'))['rating__sum'] or 0
        if author := getattr(self, 'author', False):
            rating += 3 * author.post_set.aggregate(Sum('rating'))['rating__sum'] or 0
            rating += author.post_set.aggregate(Sum('comment__rating'))['comment__rating__sum'] or 0
        self.rating = rating

    def __str__(self):
        return self.user.username


class Category(models.Model):
    category = models.CharField(max_length=64, unique=True, help_text=_('category'))

    def __str__(self):
        return self.category


class Post(models.Model):
    puser = models.ForeignKey(Puser, on_delete=models.CASCADE)
    article = models.BooleanField()
    date = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=255)
    text = models.TextField()
    rating = models.IntegerField(default=0)
    category = models.ManyToManyField(Category, through='PostCategory')

    def like(self):
        self.rating += 1

    def dislike(self):
        self.rating -= 1

    def preview(self):
        return self.text[:124] + '...'

    def get_absolute_url(self):
        return reverse('post_detail', args=[str(self.pk)])

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        cache.delete(f'Post-{self.pk}')


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    puser = models.ForeignKey(Puser, on_delete=models.CASCADE)
    text = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating += 1

    def dislike(self):
        self.rating -= 1


