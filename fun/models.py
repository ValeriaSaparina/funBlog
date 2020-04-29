from django.contrib.auth.models import User
from django.db import models


class Author(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    about = models.CharField(max_length=256, blank=True)
    count_posts = models.IntegerField(default=0)
    count_fav = models.IntegerField(default=0)
    fav = models.TextField()
    my_fav = models.TextField()


class Post(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    text = models.TextField()
    title = models.CharField(max_length=100)
    count_like = models.IntegerField(default=0)
    count_comment = models.IntegerField(default=0)
    pub_date = models.DateTimeField()
    themes = models.CharField(max_length=20, blank=True)
    tags = models.CharField(max_length=20, blank=True)


class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    text = models.TextField()
    pub_date = models.DateTimeField()
