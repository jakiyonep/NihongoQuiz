from django.db.models import Count, Q
from django.http import Http404
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from quiz.models import Quiz, Category, Tag


# Create your views here.

class Index(ListView):
    model = Quiz
    template_name = 'quiz/index.html'


class QuizDetailView(DetailView):
    model = Quiz

    def get_object(self, gueryset=None):
        obg = super().get_object(queryset=queryset)
        if not obj.public and not self.request.user.is_authenticated:
            raise Http404
        return obj

class CategoryListView(ListView):
    queryset = Category.objects.annotate(
        num_posts=Count('quiz', filter=Q(quiz__public=True))
    )

class TagListView(ListView):
    queryset = Tag.objects.annotate(
        num_posts = Count('quiz', filter = Q(quiz__public=True))
    )