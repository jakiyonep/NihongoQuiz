from django.db.models import Count, Q
from django.http import Http404
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.shortcuts import get_object_or_404

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


class CategoryPostView(ListView):
    model = Quiz
    template_name = 'quiz/category_post.html'

    def get_queryset(self):
        category_slug = self.kwargs['category_slug']
        self.category = get_object_or_404(Category, slug=category_slug)
        qs = super().get_queryset().filter(category=self.category)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.category
        return context

class TagPostView(ListView):
    model = Quiz
    template_name = 'quiz/tag_post.html'

    def get_queryset(self):
        tag_slug = self.kwargs['tag_slug']
        self.tag = get_object_or_404(Tag, slug=tag_slug)
        qs = super().get_queryset().filter(tags=self.tag)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tag'] = self.tag
        return context



class SearchPostView(ListView):
    model = Quiz
    template_name = 'quiz/search_post.html'
    paginate_by = 3

    def get_queryset(self):
        query = self.request.GET.get('q', None)
        lookups = (
            Q(question__icontains=query) |
            Q(description__icontains=query) |
            Q(category__name__icontains=query) |
            Q(tags__name__icontains=query)
        )
        if query is not None:
            qs = super().get_queryset().filter(lookups).distinct()
            return qs
        qs = super().get_queryset()
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query = self.request.GET.get('q')
        context['query'] = query
        return context