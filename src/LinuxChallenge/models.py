import pprint
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.timezone import now as timezone_now


class User(AbstractUser):
    """ユーザ"""

    def __str__(self):
        return self.username

    @property
    def points(self):
        user_correct_answer = Answer.objects.filter(user=self).exclude(flag=None)
        return sum([answer.flag.point for answer in user_correct_answer])

    @property
    def last_correct_answer_time(self):
        pprint.pprint(self)
        try:
            last_time = Answer.objects.filter(user=self).exclude(flag=None).latest().scored_time
        except Answer.DoesNotExist:
            try:
                last_time = Answer.objects.filter(user=self).exclude(flag=None).latest().scored_time
            except Answer.DoesNotExist:
                last_time = self.date_joined
        return last_time


class Level(models.Model):
    """問題のレベル"""
    stage = models.IntegerField('レベル')
    stage_limit_point = models.IntegerField('表示制限ポイント')

    def __str__(self):
        return str(self.stage)


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
    correct_answer = models.CharField('フラグ', max_length=255, unique=True)
    point = models.IntegerField('得点')
    question = models.ForeignKey(Question, verbose_name='問題')

    class Meta:
        ordering = ['question']

    def __str__(self):
        return self.correct_answer


class Answer(models.Model):
    """ユーザの解答"""
    user = models.ForeignKey(User, verbose_name='解答者')
    question = models.ForeignKey(Question, verbose_name='問題')
    user_answer = models.CharField('解答', max_length=255)
    flag = models.ForeignKey('Flag', blank=True, null=True)
    scored_time = models.DateTimeField("解答日時", blank=True, auto_now_add=True)

    class Meta:
        ordering = ['scored_time']
        get_latest_by = 'scored_time'
        unique_together = (('user', 'flag'), )

    def __str__(self):
        return self.user_answer


class Notice(models.Model):
    title = models.CharField('タイトル', max_length=255)
    sentence = models.TextField("内容")
    published_time = models.DateTimeField("公開された時間", default=timezone_now)

    class Meta:
        ordering = ["-published_time"]
