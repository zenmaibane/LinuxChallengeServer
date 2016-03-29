from django.contrib import admin
from LinuxChallenge.models import User, Level, Question, Flag, Answer, Notice


class UserAdmin(admin.ModelAdmin):
    list_display = ('username',)
    list_display_links = ('username',)
admin.site.register(User, UserAdmin)


class LevelAdmin(admin.ModelAdmin):
    list_display = ('stage',)
    list_display_links = ('stage',)
admin.site.register(Level, LevelAdmin)


class QuestionAdmin(admin.ModelAdmin):
    list_display = ('level', 'title', 'sentence')
    list_display_links = ('level', 'title', 'sentence')
admin.site.register(Question, QuestionAdmin)


class FlagAdmin(admin.ModelAdmin):
    list_display = ('correct_answer', 'point', 'question',)
    list_display_links = ('correct_answer', 'point', 'question',)
admin.site.register(Flag, FlagAdmin)


class NoticeAdmin(admin.ModelAdmin):
    list_display = ('title', 'sentence', 'published_time')
    list_display_links = ('title', 'sentence', 'published_time')
admin.site.register(Notice, NoticeAdmin)


class AnswerAdmin(admin.ModelAdmin):
    list_display = ('user', 'question', 'user_answer', 'flag', 'time')
    list_display_links = ('user', 'question', 'user_answer', 'flag', 'time')
admin.site.register(Answer, AnswerAdmin)
