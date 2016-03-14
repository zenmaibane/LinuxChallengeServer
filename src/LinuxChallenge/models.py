from django.db import models


class User(models.Model):
    """ユーザ"""
    name = models.CharField(max_length=31)
    password = models.CharField('パスワード', max_length=127)
    point = models.IntegerField('合計点')


class Level(models.Model):
    """問題のレベル"""
    level = models.IntegerField('レベル')


class Question(models.Model):
    """問題"""
    level = models.ForeignKey(Level, verbose_name='レベル')
    title = models.CharField('title', max_length=50, unique=True)
    sentence = models.TextField("問題文")


class Flag(models.Model):
    """正解のフラグ"""
    flag = models.CharField('フラグ', max_length=255)
    point = models.IntegerField('得点')
    question = models.ForeignKey(Question, verbose_name='問題')


class Answer(models.Model):
    """ユーザの解答"""
    user = models.ForeignKey(User, verbose_name='解答者')
    question = models.ForeignKey(Question, verbose_name='問題')
    userAnswer = models.CharField('解答', max_length=255)
    flag = models.ForeignKey('Flag', blank=True, null=True)





















