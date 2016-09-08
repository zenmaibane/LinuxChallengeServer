from django.contrib.messages import error, success
from django.core.urlresolvers import reverse, reverse_lazy
from django.shortcuts import redirect, get_object_or_404
from django.views.generic import CreateView, DetailView, ListView
from django.views.generic import RedirectView
from django.views.generic.edit import FormMixin

from LinuxChallenge.forms import SignUpForm, AnswerForm
from LinuxChallenge.models import User, Question, Flag, Level, Answer, Notice


class IndexView(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        if self.request.user.is_authenticated():
            return reverse('questions')
        return reverse('login')


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
                answers = Answer.objects.filter(user=self.request.user, question=question)
                correct_answers = filter(lambda answer: answer.flag is not None, answers)
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


class QuestionView(FormMixin, DetailView):
    model = Question
    template_name = "question/detail.html"
    queryset = Question.objects.all()
    form_class = AnswerForm

    def get_queryset(self):
        queryset = self.queryset

        # only answerable level's questions
        exclude_levels = Level.objects.filter(stage_limit_point__gt=self.request.user.points)

        for level in exclude_levels:
            queryset = queryset.exclude(level=level)
        return queryset

    def get_context_data(self, **kwargs):
        kwargs = super(QuestionView, self).get_context_data(**kwargs)
        key = self.get_context_object_name(self.object)
        question = self.object
        answers = Answer.objects.filter(user=self.request.user, question=question).exclude(flag=None)
        question_correct_answer_points = sum([a.flag.point for a in answers])
        obj = {
            "question": self.object,
            "is_clear": self.object.points == question_correct_answer_points,
        }
        kwargs["object"] = obj
        if key:
            kwargs[key] = obj

        return kwargs


class AccountCreateView(CreateView):
    model = User
    form_class = SignUpForm
    template_name = "signup.html"
    success_url = reverse_lazy('index')


class AnswerView(CreateView):
    model = Answer
    form_class = AnswerForm

    def get_success_url(self):
        return reverse("question", kwargs={"pk": self.kwargs["pk"]})

    def form_valid(self, form):
        form.instance.question = get_object_or_404(Question, id=self.kwargs["pk"])
        form.instance.user = self.request.user

        try:
            flag = Flag.objects.get(question=form.instance.question, correct_answer=form.cleaned_data["user_answer"])
            form.instance.flag = flag
        except Flag.DoesNotExist:
            error(self.request, "Oops, incorrect...")
            pass

        if form.instance.flag is not None:
            if Answer.objects.filter(user=self.request.user, question=form.instance.question,
                                     flag=form.instance.flag).exists():
                error(self.request, "Duplicate answer, search any?")
                return self.form_invalid(form)

            success(self.request, "Congrats, You got %d pt." % form.instance.flag.point)

        return super(AnswerView, self).form_valid(form)

    def get(self, request, *args, **kwargs):
        return redirect(reverse('question', kwargs={"pk": self.kwargs["pk"]}))

    def form_invalid(self, form):
        return redirect(reverse('question', kwargs={"pk": self.kwargs["pk"]}))


class NoticeView(ListView):
    template_name = "notice.html"
    model = Notice

