from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType


class User(AbstractUser):
    pass

class Following(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name='user',
                                on_delete=models.CASCADE)
    followed_by = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='followed_by')

    class Meta:
        ordering = ['user',]

    def __str__(self):
        return f'{self.user}'



class Posts(models.Model):
    body = models.TextField()
    creator = models.ForeignKey(settings.AUTH_USER_MODEL,
                    on_delete=models.CASCADE,
                    related_name='creator')
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date',]

    def __str__(self):
        return f'{self.body}'

    def serialize(self):
        return {
            'body': self.body,
            'creator': self.creator,
            'date': self.date,
            'comments': self.comment_post.all(),
        }



class Likes(models.Model):
    post = models.OneToOneField(Posts, related_name='post',
                                on_delete=models.CASCADE)
    liked_by = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='liked_by')

    class Meta:
        ordering = ['post',]

    def __str__(self):
        return f'{self.post}'



class Comments(models.Model):
    body = models.CharField(max_length=250)
    comment_post = models.ForeignKey(Posts, on_delete=models.CASCADE,
                             related_name='comment_post')

    comment_creator = models.ForeignKey(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE,
                                related_name='comment_creator',
                                null=True, blank=True)

    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date',]

    def __str__(self):
        return f'{self.body}'

    def serialize(self):
        return {
            'body': self.body,
            'post': self.comment_post,
            'creator': self.comment_creator,
            'date': self.date,
        }


class LikesComment(models.Model):
    comment = models.OneToOneField(Comments, related_name='comment',
                                on_delete=models.CASCADE)
    commentliked_by = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='commentliked_by')

    class Meta:
        ordering = ['comment',]

    def __str__(self):
        return f'{self.comment}'

