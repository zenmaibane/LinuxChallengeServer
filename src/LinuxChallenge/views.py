from django.shortcuts import render
from django.http.response import HttpResponse


def hello_world(request):
    return HttpResponse('Hello_world')


def hello_template(request):
    tsurai = {
        'dame': 'いやよく見たらなんかむかつく',
        'oaa': 'Python難しい.....難しくない....？',
    }
    return render(request, 'index.html', tsurai)



