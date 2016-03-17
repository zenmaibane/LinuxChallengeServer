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
from LinuxChallenge.views import IndexView, RankingView, ChallengeView, QuestionDetailView
from django.contrib import admin
from django.contrib.auth import views as auth_views


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', auth_views.login),
    url(r'^ranking/', RankingView.as_view()),
    url(r'^challenge/', ChallengeView.as_view()),
    # ?P<何か>という書き方は，viewに対してurlについている数値を何と言う名前の変数に入れて渡せばいいのかを指定するもの．
    # 例えば，以下のようなURLにアクセスしたなら……
    #     http://picture-of.pro/questions/1
    # pkという変数には，1という数値が代入されます．
    # ちなみに，DetailViewでは，pkという変数にPrimaryKeyになる値（Djangoではidですが……）を代入するように書くと
    # 自動で検索して，objectをセットしてくれます．
    url(r'^questions/(?P<pk>\d+)$', QuestionDetailView.as_view())
]


