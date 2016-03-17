from django.views.generic import TemplateView, CreateView,DetailView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from LinuxChallenge.models import User
from LinuxChallenge.models import Question


class IndexView(TemplateView):
    template_name = 'index.html'


class RankingView(TemplateView):
    template_name = 'ranking.html'


class ChallengeView(TemplateView):
    template_name = 'challenge.html'


class AuthView(LoginRequiredMixin, TemplateView):
    login_url = '/'


class AccountCreateView(CreateView):
    model = User
    form_class = UserCreationForm


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


