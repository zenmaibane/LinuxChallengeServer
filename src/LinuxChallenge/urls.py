"""LinuxChallenge URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, patterns, include
from django.contrib.auth import views as auth_view
from LinuxChallenge import views
from LinuxChallenge.views import IndexView, ChallengeView, RankingView, AccountCreateView, QuestionDetailView, AnswerView, NoticeView
from django.contrib import admin
from django.contrib.auth.decorators import login_required

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', IndexView.as_view(), name="Index"),
    url(r'^login/', views.login, name="login"),
    url(r'^logout/', auth_view.logout_then_login, name="logout"),
    url(r'^ranking/', login_required(RankingView.as_view()), name='ranking'),
    url(r'^signup/', AccountCreateView.as_view(), name='signup'),
    url(r'^challenge/', login_required(ChallengeView.as_view()), name='challenge'),
    url(r'^notice/', NoticeView.as_view(), name='notice'),
    url(r'^questions/(?P<pk>\d+)$', login_required(QuestionDetailView.as_view()), name="question"),
    url(r'^answer/', login_required(AnswerView.as_view()), name='answer')
]


