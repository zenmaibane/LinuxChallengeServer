from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """ユーザ"""
    point = models.IntegerField('合計点', blank=True, default=0)

    def __str__(self):
        return self.username


class Level(models.Model):
    """問題のレベル"""
    stage = models.IntegerField('レベル')

    def __str__(self):
        return self.stage


class Question(models.Model):
    """問題"""
    level = models.ForeignKey(Level, verbose_name='レベル', related_name="questions")
    title = models.CharField('title', max_length=50, unique=True)
    sentence = models.TextField("問題文")

    def __str__(self):
        return self.title

    @property
    def points(self):
        return sum([o.point for o in self.flag_set.all()])


class Flag(models.Model):
    """正解のフラグ"""
    flag = models.CharField('フラグ', max_length=255, unique=True)
    point = models.IntegerField('得点')
    question = models.ForeignKey(Question, verbose_name='問題')

    def __str__(self):
        return self.flag


class Answer(models.Model):
    """ユーザの解答"""
    user = models.ForeignKey(User, verbose_name='解答者')
    question = models.ForeignKey(Question, verbose_name='問題')
    user_answer = models.CharField('解答', max_length=255)
    flag = models.ForeignKey('Flag', blank=True, null=True)

    def __str__(self):
        return self.userAnswer





















