from django.contrib.auth import views
from django.core.urlresolvers import reverse
from django.views.generic import View, TemplateView, CreateView, DetailView, ListView
from LinuxChallenge.models import User, Question, Flag, Level, Answer
from LinuxChallenge.forms import SignUpForm, FlagForm
from django.shortcuts import render, render_to_response, redirect
from django.contrib.messages import error, success
from django.template import RequestContext
from django.http import HttpRequest
import datetime


class IndexView(View):
    def get(self, request, *args, **kwargs):
        user = request.user
        if user.is_authenticated():
            return redirect(reverse("challenge"))
        return redirect(reverse("login"))


class RankingView(ListView):
    template_name = 'ranking.html'

    def get_queryset(self):
        queryset = sorted(User.objects.all(), key=lambda user: (-user.points, user.last_correct_answer_time))
        return queryset


class ChallengeView(View):
    def get(self, request):
        user = request.user
        questions_per_level = []
        l = Level.objects.all()
        limit = self.user_achieved_level(request)
        for i, lev in enumerate(l):
            if i <= limit:
                questions = Question.objects.filter(level__stage=lev.stage)
                questions_array = []
                for question in questions:
                    # print("dddddd")
                    # print(question)
                    questions_array.append(question)
                    get_points = 0
                    for flag in question.flag_set.all():
                        try:
                            answer = Answer.objects.get(user=user, flag=flag)
                            get_points += answer.flag.point
                        except Answer.DoesNotExist:
                            pass
                    questions_array.append({"q": question, "get_points": get_points})
                questions_per_level.append({"levels": lev, "questions": questions_array})
            else:
                break
        return render(request=request, template_name="challenge.html",
                      dictionary={"questions_per_lev": questions_per_level},
                      context_instance=RequestContext(request))

    def user_achieved_level(self, request):
        points = request.user.points
        level = Level.objects.all()
        return_lev = 0
        for l in level:
            if points >= l.stage_limit_point:
                return_lev = l.stage
            else:
                break
        return return_lev


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
        user = request.user
        self.object = self.get_object()
        if user.points >= self.object.level.stage_limit_point:
            context = self.get_context_data(object=self.object)
            form = FlagForm(initial={"q_id": self.object.id})
            return render_to_response(template_name='question.html',
                                      dictionary={"form": form, "question": self.object},
                                      context_instance=RequestContext(request))
        else:
            return redirect(reverse("challenge"))


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
                answer = Answer(user=user, question=question, user_answer=user_answer, flag=None,
                                time=datetime.datetime.now())
                answer.save()
                error(request, "That's incorrect.")
                return redirect(question_page)
            # 回答の重複処理
            if flag and Answer.objects.filter(user=user, question=question, flag=flag).exists():
                error(request, "The flag is already submitted.")
                return redirect(question_page)
            success(request, "Correct! You got " + str(flag.point) + " points !!!")
            answer = Answer(user=user, question=question, user_answer=user_answer, flag=flag,
                            time=datetime.datetime.now())
            answer.save()
            return redirect(question_page)
        return self.get(request=request)

    def get(self, request, *args, **kwargs):
        ref_page = request.META.get('HTTP_REFERER', None)
        if ref_page is None:
            return redirect(reverse("challenge"))
        return ref_page


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
