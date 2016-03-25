from django.contrib import admin
from LinuxChallenge.models import User, Level, Question, Flag, Answer


class UserAdmin(admin.ModelAdmin):
    list_display = ('point',)
    list_display_links = ('point',)
admin.site.register(User, UserAdmin)


class LevelAdmin(admin.ModelAdmin):
    list_display = ('stage',)
    list_display_links = ('stage',)
admin.site.register(Level, LevelAdmin)


class QuestionAdmin(admin.ModelAdmin):
    list_display = ('level', 'title', 'sentence',)
    list_display_links = ('level',)
admin.site.register(Question, QuestionAdmin)


class FlagAdmin(admin.ModelAdmin):
    list_display = ('correct_answer', 'point', 'question',)
    list_display_links = ('correct_answer', 'point', 'question',)
admin.site.register(Flag, FlagAdmin)


class AnswerAdmin(admin.ModelAdmin):
    list_display = ('user', 'question', 'user_answer', 'flag',)
    list_display_links = ('user', 'question', 'user_answer', 'flag',)
admin.site.register(Answer, AnswerAdmin)
