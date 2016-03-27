from django.contrib.auth import views
from django.core.urlresolvers import reverse
from django.views.generic import View, TemplateView, CreateView, DetailView
from LinuxChallenge.models import User, Question, Flag, Level, Answer
from LinuxChallenge.forms import SignUpForm, FlagForm
from django.shortcuts import render, render_to_response, redirect
from django.contrib.messages import error, success
from django.template import RequestContext


class IndexView(View):
    def get(self, request, *args, **kwargs):
        user = request.user
        if user.is_authenticated():
            return redirect(reverse("challenge"))
        return redirect(reverse("login"))


class RankingView(TemplateView):
    template_name = 'ranking.html'


class ChallengeView(View):
    def get(self, request):
        user = request.user
        answers__per_level = []
        questions_per_level = []
        l = Level.objects.all()
        for lev in l:
            questions = Question.objects.filter(level__stage__exact=lev.stage)
            questions_array = []
            for question in questions:
                questions_array.append(question)
                acquired_points = 0
                for flag in question.flag_set.all():
                    try:
                        answer = Answer.objects.get(user=user, flag=flag)
                        acquired_points += answer.flag.point
                    except Answer.DoesNotExist:
                        pass
                questions_array.append({"q": question, "acquired_points": acquired_points})
            questions_per_level.append(
                {"levels": lev, "questions": questions_array})
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
class QuestionDetailView(DetailView):
    # 表示するモデルの種類を指定する．
    # ここでは，Questionの中でも一つを表示するのでQuestionを指定する．．
    model = Question

    # 表示するテンプレートはquestion.html．
    # ちなみに，template内ではobjectという変数に検索結果が与えられるらしい．
    # http://shinriyo.hateblo.jp/entry/2015/02/28/Django%E3%81%AEDetailView%E3%81%AE%E3%83%86%E3%83%B3%E3%83%97%E3%83%AC%E3%83%BC%E3%83%88
    # def get(self, request, *args, **kwargs):
    #     self.object = self.get_object()
    #     context = self.get_context_data(object=self.object)
    #     form = FlagForm(initial={"answer": "", "q_id": self.object.id})
    #     return render_to_response(template_name='question.html',
    #                               dictionary={"form": form, "question": self.object}, context=context)

    def get(self, request, *args, **kwargs):
        print(request.path)
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        form = FlagForm(initial={"q_id": self.object.id})
        return render_to_response(template_name='question.html',
                                  dictionary={"form": form, "question": self.object},
                                  context_instance=RequestContext(request))


class AnswerView(View):
    def post(self, request):
        form = FlagForm(request.POST)
        if form.is_valid():
            user = request.user
            q_id = form.cleaned_data['q_id']
            question = Question.objects.get(id=q_id)
            user_answer = form.cleaned_data['answer']
            question_page = "/questions/" + str(q_id)
            try:
                flag = Flag.objects.get(question=question, correct_answer__exact=user_answer)
            except Flag.DoesNotExist:
                answer = Answer(user=user, question=question, user_answer=user_answer, flag=None)
                answer.save()
                error(request, "That's incorrect.")
                return redirect(question_page)
            # 回答の重複処理
            if flag and Answer.objects.filter(user=user, question=question, flag=flag).exists():
                error(request, "The flag is already submitted.")
                return redirect(question_page)
            success(request, "Correct!")
            answer = Answer(user=user, question=question, user_answer=user_answer, flag=flag)
            answer.save()
            return redirect(question_page)


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
