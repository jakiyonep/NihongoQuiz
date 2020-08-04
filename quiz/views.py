from django.db.models import Count, Q
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import CreateView
from django.contrib import messages
from django.http import Http404
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.shortcuts import get_object_or_404, render, redirect
from django.core.paginator import Paginator
from quiz.forms import Correction
from . import forms
from django.shortcuts import render, get_object_or_404, redirect, resolve_url

from quiz.models import *
from quiz.forms import CommentForm,ReplyForm

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

    paginator = Paginator(filtered_quiz.qs, 2)
    page_number = request.GET.get('page')
    quiz_page_obj = paginator.get_page(page_number)

    context['quiz_page_obj'] = quiz_page_obj



    return render(request, 'quiz/quizzes/index.html', context)




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


def LevelPost(request, level_slug):
    quiz_list = Quiz.objects.all()
    selected_level = get_object_or_404(Level, slug=level_slug)
    selected_level_quiz_list = quiz_list.filter(level__slug=level_slug)

    # Create a paginator to split your products queryset
    paginator = Paginator(selected_level_quiz_list, 10)
    # Get the current page number
    page = request.GET.get('page')
    # Get the current slice (page) of products
    selected_level_quiz_list = paginator.get_page(page)
    num = request.GET.get('page')
    page_obj = paginator.get_page(num)

    return render(request, 'quiz/quizzes/level_post.html', {
        'object_list': selected_level_quiz_list,
        'page_obj': page_obj,
        'num': num,
        'paginator': paginator,
        'selected_level': selected_level,
    })



def CategoryPost(request, category_slug):
    quiz_list = Quiz.objects.all()
    selected_category = get_object_or_404(Category, slug=category_slug)
    selected_category_quiz_list = quiz_list.filter(category__slug=category_slug)

    # Create a paginator to split your products queryset
    paginator = Paginator(selected_category_quiz_list, 10)
    # Get the current page number
    page = request.GET.get('page')
    # Get the current slice (page) of products
    selected_category_quiz_list = paginator.get_page(page)
    num = request.GET.get('page')
    page_obj = paginator.get_page(num)

    return render(request, 'quiz/quizzes/category_post.html', {
        'object_list': selected_category_quiz_list,
        'page_obj': page_obj,
        'num': num,
        'paginator': paginator,
        'selected_category': selected_category,
    })


def TagPost(request, tag_slug):
    quiz_list = Quiz.objects.all()
    selected_tag = get_object_or_404(Tag, slug=tag_slug)

    selected_tag_quiz_list = quiz_list.filter(tags__slug=tag_slug)

    # Create a paginator to split your products queryset
    paginator = Paginator(selected_tag_quiz_list, 10)
    # Get the current page number
    page = request.GET.get('page')
    # Get the current slice (page) of products
    selected_category_quiz_list = paginator.get_page(page)
    num = request.GET.get('page')
    page_obj = paginator.get_page(num)

    return render(request, 'quiz/quizzes/tag_post.html', {
        'object_list': selected_category_quiz_list,
        'page_obj': page_obj,
        'num': num,
        'paginator': paginator,
        'selected_tag': selected_tag,
    })


def QuizSearchList(request):
    quiz_search_list = Quiz.objects.all()
    query = request.GET.get('q')

    if query:
        quiz_search_list = Quiz.objects.filter(
            Q(question__icontains=query) |
            Q(choice1__icontains=query) |
            Q(choice2__icontains=query) |
            Q(choice3__icontains=query) |
            Q(choice4__icontains=query)
        ).distinct()

    # Create a paginator to split your products queryset
    paginator = Paginator(quiz_search_list, 10)
    # Get the current page number
    page = request.GET.get('page')
    # Get the current slice (page) of products
    article_list = paginator.get_page(page)
    num = request.GET.get('page')
    page_obj = paginator.get_page(num)

    return render(request, 'quiz/quizzes/search_post.html', {
        'object_list': quiz_search_list,
        'page_obj': page_obj,
        'num': num,
        'paginator': paginator,
        'query': query,
    })



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

def ArticleList(request):
    article_list = Articles.objects.all()
    query = request.GET.get('q')

    if query:
        article_list = Articles.objects.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query)
        ).distinct()

    # Create a paginator to split your products queryset
    paginator = Paginator(article_list, 10)
    # Get the current page number
    page = request.GET.get('page')
    # Get the current slice (page) of products
    article_list = paginator.get_page(page)
    num = request.GET.get('page')
    page_obj = paginator.get_page(num)

    return render(request, 'quiz/articles/articles_index.html', {
        'article_list': article_list,
        'page_obj': page_obj,
        'num': num,
        'paginator': paginator,
    })


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


class CommentFormView(CreateView):
    model = Comment
    form_class = CommentForm
    template_name = 'quiz/articles/comment/comment_form.html'

    def form_valid(self, form):
        comment = form.save(commit=False)
        post_pk = self.kwargs['pk']
        comment.article = get_object_or_404(Articles, pk=post_pk)
        comment.save()
        article_title_slug = comment.article.title_slug
        return redirect('quiz:article_post', title_slug=article_title_slug)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post_pk = self.kwargs['pk']
        context['post'] = get_object_or_404(Articles, pk=post_pk)
        return context


@login_required
def comment_approve(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.approve()
    article_title_slug = comment.article.title_slug
    return redirect('quiz:article_post', title_slug=article_title_slug)


@login_required
def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.delete()

    article_title_slug = comment.article.title_slug
    return redirect('quiz:article_post', title_slug=article_title_slug)


class ReplyFormView(CreateView):
    model = Reply
    form_class = ReplyForm
    template_name = 'quiz/articles/comment/reply_form.html'

    def form_valid(self, form):
        reply = form.save(commit=False)
        comment_pk = self.kwargs['pk']
        reply.comment = get_object_or_404(Comment, pk=comment_pk)
        reply.save()
        article_title_slug = reply.comment.article.title_slug
        return redirect('quiz:article_post', title_slug=article_title_slug)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        comment_pk = self.kwargs['pk']
        context['comment'] = get_object_or_404(Comment, pk=comment_pk)
        return context


@login_required
def reply_approve(request, pk):
    reply = get_object_or_404(Reply, pk=pk)
    reply.approve()
    article_title_slug = reply.comment.article.title_slug
    return redirect('quiz:article_post', title_slug=article_title_slug)


@login_required
def reply_remove(request, pk):
    reply = get_object_or_404(Reply, pk=pk)
    reply.delete()
    article_title_slug = reply.comment.article.title_slug
    return redirect('quiz:article_post', title_slug=article_title_slug)

""""
class SearchArticleVIew(ListView):
    model = Articles
    template_name = 'quiz/articles/article_post.html'

    def get_queryset(self):
        query = self.request.GET.get('q', None)
        lookups = (
                Q(title__icontains=query) |
                Q(category2__slug__icontains=query) |
                Q(content__icontains=query)
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
"""





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
            print("検証に成功しました。データを保存します")
            return render(request, 'quiz/corrections/after_submit.html')
        else:
            print("検証に失敗したので、データを保存しません。検証に失敗した理由を次に表示します。")
            print(form.errors)

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


