from django.contrib.auth import views
from django.core.urlresolvers import reverse
from django.views.generic import View, TemplateView, CreateView, DetailView, ListView
from django.views.generic.edit import FormMixin
from django.http import HttpResponse
# from django.contrib.auth.forms import UserCreationForm
from LinuxChallenge.models import User, Question, Flag, Level, Answer
from LinuxChallenge.forms import SignUpForm, FlagForm
from django.shortcuts import render, render_to_response


class IndexView(TemplateView):
    template_name = "index.html"


class RankingView(TemplateView):
    template_name = 'ranking.html'


# class ChallengeView(ListView):
#     template_name = 'challenge.html'
#     model = Flag


class ChallengeView(View):
    def get(self, request):
        questions_per_level = []
        l = Level.objects.all()
        for lev in l:
            questions_per_level.append(
                {"levels": lev, "questions": Question.objects.filter(level__stage__exact=lev.stage)})
        return render(request=request, template_name="challenge.html",
                      dictionary={"questions_per_lev": questions_per_level})


class AccountCreateView(CreateView):
    model = User
    form_class = SignUpForm
    template_name = "signup.html"

    def get_success_url(self):
        return reverse("Index")


# 単純に保存特定のデータを取り出すView = 個別のオブジェクトを取り出すView
# であるので，DetailViewを利用すると可能．ので，継承してパラメータを変え利用する．
# http://docs.djangoproject.jp/en/latest/ref/class-based-views.html#detailview
class QuestionDetailView(DetailView, FormMixin):
    # 表示するモデルの種類を指定する．
    # ここでは，Questionの中でも一つを表示するのでQuestionを指定する．．
    model = Question
    form_class = FlagForm
    # 表示するテンプレートはquestion.html．
    # ちなみに，template内ではobjectという変数に検索結果が与えられるらしい．
    # http://shinriyo.hateblo.jp/entry/2015/02/28/Django%E3%81%AEDetailView%E3%81%AE%E3%83%86%E3%83%B3%E3%83%97%E3%83%AC%E3%83%BC%E3%83%88
    template_name = 'question.html'
    # object = Question.objects.get(id=pk)
    # render(template_name, object)


class AnswerView(View):
    def post(self, request):
        form = FlagForm(request.POST)
        if form.is_valid():
            user = request.user
            q_id = form.cleaned_data['q_id']
            question = Question.objects.filter(id=q_id)
            url = "question/"+q_id
            user_answer = form.cleaned_data['answer']
            flag = Flag.objects.filter(question=question, flag=user_answer)
            answer = Answer(user=user, question=question, user_answer=user_answer, flag=flag)
            if flag is None:
                answer.save()
                is_correct = False
                return render(request=request, template_name=url,
                              dictionary={"is_correct": is_correct})

            if flag and Answer.objects.filter(user=user, question=question, flag=flag).exists():
                is_duplicate = True
                return render(request=request, template_name=url,
                              dictionary={"is_duplicate": is_duplicate})
            answer.save()
            is_correct = True
            return render(request=request, template_name=url,
                          dictionary={"is_correct": is_correct})


def login(request):
    return views.login(request=request, template_name='index.html', redirect_field_name='challenge.html')


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
