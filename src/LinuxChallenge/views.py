import datetime
from pprint import pprint

from django.contrib.auth import views
from django.contrib.messages import error, success
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.views.generic import View, CreateView, DetailView, ListView
from django.views.generic.edit import BaseCreateView

from LinuxChallenge.forms import SignUpForm, FlagForm, AnswerForm
from LinuxChallenge.models import User, Question, Flag, Level, Answer, Notice


class IndexView(View):
    def get(self, request, *args, **kwargs):
        user = request.user
        if user.is_authenticated():
            return redirect(reverse("challenge"))
        return redirect(reverse("login"))


class RankingView(ListView):
    template_name = 'ranking.html'

    def get_queryset(self):
        queryset = sorted(User.objects.exclude(is_staff=True),
                          key=lambda user: (-user.points, user.last_correct_answer_time))
        return queryset


class QuestionsView(ListView):
    queryset = Question.objects.all()
    template_name = 'question/list.html'

    def get_context_data(self, **kwargs):
        # <data structure>
        # objects = [{
        #   level: level,
        #   questions: level_questions=[{
        #           question: Question,
        #           scored_points: int
        #   }]
        # }]

        objects = list()

        # only answerable levels
        for level in Level.objects.filter(stage_limit_point__lte=self.request.user.points):
            level_questions = list()
            for question in Question.objects.filter(level=level):
                answers = Answer.objects.filter(question=question)
                correct_answers = filter(lambda answer: answer.is_correct, answers)
                obj = {
                    "question": question,
                    "scored_points": sum([ans.flag.point for ans in correct_answers])
                }
                level_questions.append(obj)

            obj = {
                "level": level,
                "questions": level_questions
            }

            objects.append(obj)

        kwargs["objects"] = objects

        return super(QuestionsView, self).get_context_data(**kwargs)


class QuestionDetailView(DetailView):
    model = Question
    template_name = "question/detail.html"
    queryset = Question.objects.all()

    def get_queryset(self):
        queryset = self.queryset

        # only answerable level's questions
        exclude_levels = Level.objects.exclude(stage_limit_point__lt=self.request.user.points)

        for level in exclude_levels:
            queryset = queryset.exclude(level=level)

        return queryset

    def get_context_data(self, **kwargs):
        kwargs = super(QuestionDetailView, self).get_context_data(**kwargs)
        key = self.get_context_object_name(self.object)
        question = self.object
        answers = Answer.objects.filter(user=self.request.user).filter(question=question)
        question_correct_answer_points = sum(
            [a.flag.point for a in filter(lambda x: x.is_correct, answers)])
        obj = {
            "question": self.object,
            "is_correct": self.object.points == question_correct_answer_points
        }
        kwargs["object"] = obj
        if key:
            kwargs[key] = obj
        return kwargs


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
    return views.login(request=request, template_name='index.html', redirect_field_name='list.html')


def logout_then_login(request):
    return views.logout_then_login(request=request, next_page="index")


def is_EventPeriod(start, end):
    return True
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
