from django.db.models import Count, Q
from django.http import Http404
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.shortcuts import get_object_or_404, render
from django.core.paginator import Paginator
from quiz.forms import Correction
from . import forms

from quiz.models import *

from .filters import QuizFilter


# Create your views here.

class BeforeYouStart(ListView):
    model = BeforeYouStart
    template_name = 'quiz/before.html'


def QuizListView(request):
    context = {}

    filtered_quiz = QuizFilter(
        request.GET,
        queryset=Quiz.objects.all(),
    )

    context['filtered_quiz'] = filtered_quiz

    paginator = Paginator(filtered_quiz.qs, 20)
    page_number = request.GET.get('page')
    quiz_page_obj = paginator.get_page(page_number)

    context['quiz_page_obj'] = quiz_page_obj

    return render(request, 'quiz/index.html', context)


class LevelListView(ListView):
    queryset = Level.objects.annotate(
        num_posts=Count('quiz', filter=Q(quiz__public=True))
    )


class CategoryListView(ListView):
    queryset = Category.objects.annotate(
        num_posts=Count('quiz', filter=Q(quiz__public=True))
    )


class TagListView(ListView):
    queryset = Tag.objects.annotate(
        num_posts=Count('quiz', filter=Q(quiz__public=True))
    )


class LevelPostView(ListView):
    model = Quiz
    template_name = 'quiz/level_post.html'

    def get_queryset(self):
        level_slug = self.kwargs['level_slug']
        self.level = get_object_or_404(Level, slug=level_slug)
        qs = super().get_queryset().filter(level=self.level)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['level'] = self.level
        return context


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

    def get_queryset(self):
        query = self.request.GET.get('q', None)
        lookups = (
                Q(question__icontains=query) |
                Q(description__icontains=query) |
                Q(category__name__icontains=query) |
                Q(tags__name__icontains=query) |
                Q(descriptiondetail__word__icontains=query)
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


##### Basics #####

class ToppageView(TemplateView):
    template_name = 'quiz/toppage.html'


class BasicsIndex(ListView):
    model = Basics
    template_name = 'quiz/basics/basics_index.html'


class BasicsDetailView(DetailView):
    model = Basics
    template_name = 'quiz/basics/basic_post.html'
    slug_field = 'title_slug'
    slug_url_kwarg = "title_slug"

    def get_object(self, queryset=None):
        obj = super().get_object(queryset=queryset)
        if not obj.public and not self.request.user.is_authenticated:
            raise Http404
        return obj




##### Articles ######

class ArticlesIndex(ListView):
    model = Articles
    template_name = 'quiz/articles/articles_index.html'

    paginate_by = 15


class ArticleDetailView(DetailView):
    model = Articles
    template_name = 'quiz/articles/article_post.html'
    slug_field = 'title_slug'
    slug_url_kwarg = "title_slug"

    def get_object(self, queryset=None):
        obj = super().get_object(queryset=queryset)
        if not obj.public and not self.request.user.is_authenticated:
            raise Http404
        return obj

class ArticlesTagList(ListView):
    queryset = ArticlesTag.objects.annotate(
        num_posts=Count('articles', filter=Q(articles__public=True)))



class ArticleTagsView(ListView):
    model = Articles
    template_name = 'quiz/articles/article_tag_post.html'
    paginate_by = 15

    def get_queryset(self):
        article_tag_slug = self.kwargs['article_tag_slug']
        self.tag = get_object_or_404(ArticlesTag, slug=article_tag_slug)
        qs = super().get_queryset().filter(tag=self.tag)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['article_tag_slug'] = self.tag
        return context

class ArticleCategoryView(ListView):
    model = Articles
    template_name = 'quiz/articles/article_category_post.html'
    paginate_by = 15

    def get_queryset(self):
        article_category2_slug = self.kwargs['article_category2_slug']
        self.category2 = get_object_or_404(ArticlesCategory, slug=article_category2_slug)
        qs = super().get_queryset().filter(category2=self.category2)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['article_category2_slug'] = self.category2
        return context



##### Lessons ######


class LessonsIndex(ListView):
    model = Lesson
    template_name = 'quiz/lessons/lessons_index.html'


class LessonDetailView(DetailView):
    model = Lesson
    template_name = 'quiz/lessons/lesson_post.html'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset=queryset)
        if not obj.public and not self.request.user.is_authenticated:
            raise Http404
        return obj


class LessonVocabularyIndex(ListView):
    model = LessonVocabulary
    template_name = 'quiz/lessons/lesson_vocabulary.html'


class LessonGrammarIndex(ListView):
    model = LessonGrammar
    template_name = 'quiz/lessons/lesson_grammar.html'


class LessonKanjiIndex(ListView):
    model = LessonKanji
    template_name = 'quiz/lessons/lesson_kanji.html'


class CorrectionIndex(ListView):
    model = Correction
    template_name = 'quiz/corrections/correction_index.html'


def CorrectionAdd(request):
    form = forms.CorrectionForm()

    if request.method == 'POST':
        form = forms.CorrectionForm(request.POST)
        if form.is_valid():
            form.save()

            return render(request, 'quiz/corrections/after_submit.html')




    return render(request, 'quiz/corrections/correction_add.html', {'form': form})

class AfterSubmit(TemplateView):
    template_name = 'quiz/corrections/after_submit.html'

class CorrectionDetail(DetailView):
    model = Correction
    template_name = 'quiz/corrections/correction_post.html'
    slug_field = 'title_slug'
    slug_url_kwarg = "title_slug"

    def get_object(self, queryset=None):
        obj = super().get_object(queryset=queryset)
        if not obj.public and not self.request.user.is_authenticated:
            raise Http404
        return obj


