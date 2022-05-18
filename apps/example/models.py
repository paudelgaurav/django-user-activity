from django.db import models


class Post(models.Model):
    title = models.CharField(max_length=250)
    body = models.TextField()


class Article(models.Model):
    title = models.CharField(max_length=250)
    body = models.TextField()
