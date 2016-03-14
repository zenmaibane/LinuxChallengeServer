from django.views.generic import TemplateView


class IndexView(TemplateView):
    template_name = 'index.html'


class RankingView(TemplateView):
    template_name = 'ranking.html'




