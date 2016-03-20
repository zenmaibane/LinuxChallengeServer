from django.contrib.auth import views
from django.core.urlresolvers import reverse
from django.views.generic import TemplateView, CreateView, DetailView, ListView
#from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from LinuxChallenge.models import User, Question, Flag
from LinuxChallenge.forms import SignUpForm


class IndexView(TemplateView):
    template_name = "index.html"


class RankingView(TemplateView):
    template_name = 'ranking.html'


class ChallengeView(ListView):
    template_name = 'challenge.html'
    model = Question
    model2 = Flag


# class AuthView(LoginRequiredMixin, TemplateView):
#     login_url = '/'


class AccountCreateView(CreateView):
    model = User
    form_class = SignUpForm
    template_name = "signup.html"

    def get_success_url(self):
        return reverse("Index")


# 単純に特定のデータを取り出すView = 個別のオブジェクトを取り出すView
# であるので，DetailViewを利用すると可能．ので，継承してパラメータを変え利用する．
# http://docs.djangoproject.jp/en/latest/ref/class-based-views.html#detailview
class QuestionDetailView(DetailView):
    # 表示するモデルの種類を指定する．
    # ここでは，Questionの中でも一つを表示するのでQuestionを指定する．．
    model = Question

    # 表示するテンプレートはquestion.html．
    # ちなみに，template内ではobjectという変数に検索結果が与えられるらしい．
    # http://shinriyo.hateblo.jp/entry/2015/02/28/Django%E3%81%AEDetailView%E3%81%AE%E3%83%86%E3%83%B3%E3%83%97%E3%83%AC%E3%83%BC%E3%83%88
    template_name = 'question.html'
# object = Question.objects.get(id=pk)
# render(template_name, object)


def login(request):
    return views.login(request=request, template_name='index.html', redirect_field_name="challenge.html")


def logout_then_login(request):
    return views.logout_then_login(request=request, next_page="index")

"""
class HogoHogeView(mixin.SingleObjectMixin):
    def get_object(self, query_set=None):
        if user.point < query_set.level.point:
            raise ValidationError(detail="You don't have permission", 403)
        super(HogeHogeView, self).get_object(query_set)

###
# get_object()
#  -> query_set => None
# get_object(Question.objects.all)
#  ->
"""