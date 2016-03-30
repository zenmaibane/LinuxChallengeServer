import pprint

from django.contrib.auth import views
from django.core.urlresolvers import reverse
from django.views.generic import View, CreateView, DetailView, ListView
from django.views.generic.edit import BaseCreateView

from LinuxChallenge.models import User, Question, Flag, Level, Answer, Notice
from LinuxChallenge.forms import SignUpForm, FlagForm
from django.shortcuts import render, render_to_response, redirect
from django.contrib.messages import error, success
from django.template import RequestContext
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
        queryset = sorted(User.objects.exclude(is_staff=True), key=lambda user: (-user.points, user.last_correct_answer_time))
        return queryset


class ChallengeView(View):
    def get(self, request):
        user = request.user
        questions_per_level = []
        l = Level.objects.all()
        for lev in l:
            if user.points >= lev.stage_limit_point:
                questions = Question.objects.filter(level__stage=lev.stage)
                questions_array = []
                for question in questions:
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


class AccountCreateView(CreateView):
    model = User
    form_class = SignUpForm
    template_name = "signup.html"

    def get_success_url(self):
        return reverse("Index")

    def post(self, request, *args, **kwargs):
        if is_EventPeriod(None, datetime.datetime(2016, 3, 30, 20)):
            self.object = None
            return super(BaseCreateView, self).post(request, *args, **kwargs)
        else:
            error(request, "Sorry! Outside of service hours.")
            return redirect(to=reverse("signup"))


class QuestionDetailView(DetailView):
    model = Question

    def get(self, request, *args, **kwargs):
        user = request.user
        self.object = self.get_object()
        is_clear = None
        for f in self.object.flag_set.all():
            try:
                answer = Answer.objects.get(user=user, flag=f)
                is_clear = True
            except Answer.DoesNotExist:
                is_clear = False
                break
        if user.points >= self.object.level.stage_limit_point:
            form = FlagForm(initial={"q_id": self.object.id})
            return render_to_response(template_name='question.html',
                                      dictionary={"form": form, "question": self.object, "is_clear": is_clear},
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
            if is_EventPeriod(datetime.datetime(2016, 3, 30, 12), datetime.datetime(2016, 3, 30, 20)):
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
            else:
                error(request, "Sorry! Outside of service hours.")
                return redirect(question_page)

        return self.get(request=request)

    def get(self, request, *args, **kwargs):
        ref_page = request.META.get('HTTP_REFERER', None)
        if ref_page is None:
            return redirect(reverse("challenge"))
        return ref_page


class NoticeView(ListView):
    template_name = "notice.html"
    model = Notice


def login(request):
    return views.login(request=request, template_name='index.html', redirect_field_name='challenge.html')


def logout_then_login(request):
    return views.logout_then_login(request=request, next_page="index")


def is_EventPeriod(start, end):
    current_DateTime = datetime.datetime.now()
    end_DateTime = end
    if start is None:
        if current_DateTime <= end_DateTime:
            return True
        return False

    start_DateTime = start
    if start_DateTime <= current_DateTime <= end_DateTime:
        return True
    return False
