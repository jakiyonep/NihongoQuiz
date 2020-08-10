from django.contrib.auth.decorators import login_required
from django.views.generic.edit import CreateView
from django.http import Http404, HttpResponseBadRequest, HttpResponseRedirect, JsonResponse
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.core.paginator import Paginator

from quiz.forms import Correction
from . import forms
from django.shortcuts import render, get_object_or_404, redirect, resolve_url
from django.views.decorators.http import require_POST
from django.http import HttpResponse
try:
    from django.utils import simplejson as json
except ImportError:
    import json

from quiz.models import *
from quiz.forms import CommentForm,ReplyForm

from .filters import QuizFilter, ArticleFilter

from django.core.signing import BadSignature, SignatureExpired, loads, dumps
from django.template.loader import render_to_string
from django.urls import reverse_lazy, reverse
from django.views import generic
from .forms import (
    LoginForm, UserCreateForm, UserUpdateForm, MyPasswordChangeForm,
    MyPasswordResetForm, MySetPasswordForm, EmailChangeForm
)
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import (
    LoginView, LogoutView, PasswordChangeView, PasswordChangeDoneView,
    PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
)
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail, BadHeaderError
from datetime import datetime
from django.utils import timezone
from django.core.mail import send_mail
from django.shortcuts import render, get_object_or_404, redirect, resolve_url
from django.db.models import Count, Q


# Create your views here.

class BeforeYouStart(ListView):
    model = BeforeYouStart
    template_name = 'quiz/before.html'


def QuizListView(request):
    context = {}

    quiz_index_query = request.GET.get('q')

    if quiz_index_query:
        filtered_quiz = Quiz.objects.filter(
            Q(question__icontains=quiz_index_query) |
            Q(choice1__icontains=quiz_index_query) |
            Q(choice2__icontains=quiz_index_query) |
            Q(choice3__icontains=quiz_index_query) |
            Q(choice4__icontains=quiz_index_query)
        ).distinct()

    filtered_quiz = QuizFilter(
        request.GET,
        queryset=Quiz.objects.all(),
    )

    paginator = Paginator(filtered_quiz.qs, 10)
    page_number = request.GET.get('page')
    quiz_page_obj = paginator.get_page(page_number)

    context['quizzes'] = filtered_quiz
    context['quiz_page_obj'] = quiz_page_obj
    context['quiz_index_query'] = 1

    return render(request, 'quiz/quizzes/index.html', context)

@login_required
def QuizLike(request):
    user = request.user
    pk = request.POST.get('pk', None)
    quiz = get_object_or_404(Quiz, pk=pk)
    if request.method == 'POST':
        if quiz.likes.filter(pk=user.pk).exists():
            quiz.likes.remove(user)
            is_liked = False
        else:
            quiz.likes.add(user)
            is_liked = True
        ctx = {
            'quiz':quiz,
            'is_liked': is_liked,
            'total_likes_json': quiz.total_likes(),
        }
    if request.is_ajax():
        html = render_to_string('quiz/quizzes/like.html', ctx, request=request)
        return JsonResponse({'form':html})

def QuizPoll(request):
    user = request.user
    pk = request.POST.get('pk', None)
    quiz = get_object_or_404(Quiz, pk=pk)
    first_try = 10
    is_tried = False

    if user in quiz.answered_user.filter(pk=user.pk):
        is_tried = True

    if request.method == 'POST':
        if not quiz.answered_user.filter(pk=user.pk).exists():

            ctx = {
                'quiz': quiz,
            }

    if request.is_ajax():
        choice = request.POST['selected_choice']
        correct_choice = request.POST['correct_choice']

        if not quiz.answered_user.filter(pk=user.pk).exists():
            if choice == "1":
                quiz.choice1_count.add(user)
            if choice == "2":
                quiz.choice2_count.add(user)
            if choice == "3":
                quiz.choice3_count.add(user)
            if choice == "4":
                quiz.choice4_count.add(user)
            quiz.answered_user.add(user)


        if is_tried == False:

            if choice == correct_choice:
                quiz.first_try_correct.add(user)
                print('first_try_correct')
                first_try = 1

            else:
                print('first_try_wrong')
                first_try = 0

        else:

            if quiz.first_try_correct.filter(pk=user.pk).exists():
                print('non_first_correct')
                first_try = 1
            else:
                print('non_first_wrong')
                first_try = 0


        ctx = {
            'choice_1': quiz.choice1_count,
            'choice_2': quiz.choice2_count,
            'choice_3': quiz.choice3_count,
            'choice_4': quiz.choice4_count,
            'quiz':quiz,
            'total_user_answered': quiz.total_user_answered(),
            'first_try': first_try,
            'choice': choice,
            'correct_choice': correct_choice,
        }



        html = render_to_string('quiz/quizzes/choice_section.html', ctx, request=request)
        return JsonResponse({'form':html})

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

    quiz_list = QuizFilter(
        request.GET,
        queryset=quiz_list,
    )



    return render(request, 'quiz/quizzes/level_post.html', {
        'object_list': selected_level_quiz_list,
        'quizzes':quiz_list,
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

    quiz_list = QuizFilter(
        request.GET,
        queryset=quiz_list,
    )

    return render(request, 'quiz/quizzes/category_post.html', {
        'object_list': selected_category_quiz_list,
        'quizzes': quiz_list,
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

    quiz_list = QuizFilter(
        request.GET,
        queryset=quiz_list,
    )

    return render(request, 'quiz/quizzes/tag_post.html', {
        'object_list': selected_category_quiz_list,
        'quizzes': quiz_list,
        'page_obj': page_obj,
        'num': num,
        'paginator': paginator,
        'selected_tag': selected_tag,
    })

def QuizSearchList(request):
    quiz_search_list = Quiz.objects.all()


    # Create a paginator to split your products queryset
    paginator = Paginator(quiz_search_list, 10)
    # Get the current page number
    page = request.GET.get('page')
    # Get the current slice (page) of products
    quiz_search_list = paginator.get_page(page)
    num = request.GET.get('page')
    page_obj = paginator.get_page(num)

    return render(request, 'quiz/quizzes/search_post.html', {
        'object_list': quiz_search_list,
        'page_obj': page_obj,
        'num': num,
        'paginator': paginator,

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

    article_list = ArticleFilter(
        request.GET,
        queryset=article_list,
    )

    paginator = Paginator(article_list.qs, 10)
    page_number = request.GET.get('page')
    article_page_obj = paginator.get_page(page_number)

    return render(request, 'quiz/articles/articles_index.html', {
        'article_list': article_list,
        'page_obj': article_page_obj,
        'num': page_number,
        'paginator': paginator,
        'article_index_query': 1,
    })

@login_required
def ArticleLike(request):
    user = request.user
    pk = request.POST.get('pk', None)
    article = get_object_or_404(Articles, pk=pk)
    if request.method == 'POST':
        if article.likes.filter(pk=user.pk).exists():
            article.likes.remove(user)
            is_liked = False
            print('removed')
        else:
            article.likes.add(user)
            is_liked = True
            print('added')
        ctx = {
            'article':article,
            'is_liked': is_liked,
            'total_likes_json': article.total_likes(),
        }
    if request.is_ajax():
        print('ajax requested')
        html = render_to_string('quiz/articles/like.html', ctx, request=request)
        return JsonResponse({'form':html})

def ArticleDetail(request, title_slug):
    article = get_object_or_404(Articles, title_slug=title_slug)
    comments = Comment.objects.all()
    article_comments = comments.filter(article=article)
    context = {
        "article": article,
        "comments": article_comments,
    }

    return render(request, "quiz/articles/article_post.html", context)

class ArticlesTagList(ListView):
    queryset = ArticlesTag.objects.annotate(
        num_posts=Count('articles', filter=Q(articles__public=True)))

def ArticleTagsView(request, article_tag_slug):
    article_list = Articles.objects.all()
    selected_tag = get_object_or_404(ArticlesTag, slug=article_tag_slug)

    selected_tag_article_list = article_list.filter(tag__slug=article_tag_slug)

    article_list = ArticleFilter(
        request.GET,
        queryset=article_list,
    )

    paginator = Paginator(selected_tag_article_list, 10)
    page_number = request.GET.get('page')
    article_page_obj = paginator.get_page(page_number)

    return render(request, 'quiz/articles/article_tag_post.html', {
        'object_list': selected_tag_article_list,
        'article_list': article_list,
        'page_obj': article_page_obj,
        'num': page_number,
        'paginator': paginator,
        'selected_tag': selected_tag,
    })

def ArticleCategoryView(request, article_category2_slug):
    article_list = Articles.objects.all()
    selected_category2 = get_object_or_404(ArticlesCategory, slug=article_category2_slug)

    selected_category2_article_list = article_list.filter(category2__slug=article_category2_slug)

    article_list = ArticleFilter(
        request.GET,
        queryset=article_list,
    )

    paginator = Paginator(selected_category2_article_list, 10)
    page_number = request.GET.get('page')
    article_page_obj = paginator.get_page(page_number)

    return render(request, 'quiz/articles/article_category_post.html', {
        'object_list': selected_category2_article_list,
        'article_list': article_list,
        'page_obj': article_page_obj,
        'num': page_number,
        'paginator': paginator,
        'selected_category2': selected_category2,
    })


def CommentAdd(request):
    context={}
    if request.is_ajax():
        login_author = None
        author = request.POST['comment_author']
        comment_content = request.POST['comment_content']
        article_pk = request.POST['article_id']
        article = get_object_or_404(Articles, pk=article_pk)
        if request.user.is_authenticated:
            login_author = request.user
            print(login_author)
        comment = Comment(
            article = article,
            author = author,
            text = comment_content,
            timestamp = timezone.now(),
            login_author = login_author,
        )
        comment.save()
        all_comments = Comment.objects.all()
        comments = all_comments.filter(article=article)
        context = {
            'comments': comments,
        }

        html = render_to_string('quiz/articles/comment/comments.html', context, request=request)
        print('ss')
        return JsonResponse({'form':html})


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

def ReplyAdd(request):
    context={}
    if request.is_ajax():
        print('ajax start')
        login_author = None
        author = request.POST['reply_author']
        reply_content = request.POST['reply_content']
        comment_pk = request.POST['comment_id']
        comment = get_object_or_404(Comment, pk=comment_pk)
        if request.user.is_authenticated:
            login_author = request.user
            print(login_author)
        reply = Reply(
            comment = comment,
            author = author,
            text = reply_content,
            timestamp = timezone.now(),
            login_author = login_author,
        )
        reply.save()
        all_replies = Reply.objects.all()
        replies = all_replies.filter(comment=comment)
        context = {
            'ajax_replies': replies
        }

        html = render_to_string('quiz/articles/comment/replies.html', context, request=request)
        return JsonResponse({'form':html})


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

#Correction

class CorrectionIndex(ListView):
    model = Correction
    template_name = 'quiz/corrections/correction_index.html'

def CorrectionAdd(request):
    form = forms.CorrectionForm(request.POST)
    user = request.user

    if request.method == 'POST':
        form = forms.CorrectionForm(request.POST)
        if form.is_valid():
            form.save()
            print("検証に成功しました。データを保存します")
            print(user)
            if request.user.is_authenticated:
                correction = form.save(commit=False)
                correction.login_name = request.user
                correction.save()
            return render(request, 'quiz/corrections/after_submit.html')

        else:
            print("検証に失敗したので、データを保存しません。検証に失敗した理由を次に表示します。")
            print(form.errors)

    return render(request, 'quiz/corrections/correction_add.html', {
        'form': form,
    })

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


# USER REGISTRATION

User = get_user_model()


class Login(LoginView):
    """ログインページ"""
    form_class = LoginForm
    template_name = 'quiz/register/login.html'


class Logout(LogoutView):
    """ログアウトページ"""
    template_name = 'quiz/toppage.html'


class UserCreate(generic.CreateView):
    """ユーザー仮登録"""
    template_name = 'quiz/register/user_create.html'
    form_class = UserCreateForm

    def form_valid(self, form):
        """仮登録と本登録用メールの発行."""
        # 仮登録と本登録の切り替えは、is_active属性を使うと簡単です。
        # 退会処理も、is_activeをFalseにするだけにしておくと捗ります。
        user = form.save(commit=False)
        user.is_active = False
        user.save()

        # アクティベーションURLの送付
        current_site = get_current_site(self.request)
        #domain = current_site.domain
        domain = '127.0.0.1:8000'

        context = {
            'protocol': 'https' if self.request.is_secure() else 'http',
            'domain': domain,
            'token': dumps(user.pk),
            'user': user,
        }

        subject = render_to_string('quiz/mail_template/create/subject.txt', context)
        subject = subject.strip()
        message = render_to_string('quiz/mail_template/create/message.txt', context)
        user.email_user(subject, message)
        return redirect('quiz:user_create_done')


class UserCreateDone(generic.TemplateView):
    """ユーザー仮登録したよ"""
    template_name = 'quiz/register/user_create_done.html'


class UserCreateComplete(generic.TemplateView):
    """メール内URLアクセス後のユーザー本登録"""
    template_name = 'quiz/register/user_create_complete.html'
    timeout_seconds = getattr(settings, 'ACTIVATION_TIMEOUT_SECONDS', 60 * 60 * 24)  # デフォルトでは1日以内

    def get(self, request, **kwargs):
        """tokenが正しければ本登録."""
        token = kwargs.get('token')
        try:
            user_pk = loads(token, max_age=self.timeout_seconds)

        # 期限切れ
        except SignatureExpired:
            return HttpResponseBadRequest()

        # tokenが間違っている
        except BadSignature:
            return HttpResponseBadRequest()

        # tokenは問題なし
        else:
            try:
                user = User.objects.get(pk=user_pk)
            except User.DoesNotExist:
                return HttpResponseBadRequest()
            else:
                if not user.is_active:
                    # まだ仮登録で、他に問題なければ本登録とする
                    user.is_active = True
                    user.save()
                    return super().get(request, **kwargs)

        return HttpResponseBadRequest()


class OnlyYouMixin(UserPassesTestMixin):
    """本人か、スーパーユーザーだけユーザーページアクセスを許可する"""
    raise_exception = True

    def test_func(self):
        user = self.request.user
        return user.pk == self.kwargs['pk'] or user.is_superuser


def UserDetail(request, pk):
    login_author = get_object_or_404(User, pk=pk)

    #Quiz
    liked_quizzes = Quiz.objects.all().filter(likes=request.user)
    sliced_liked_quizzes = liked_quizzes[:5]
    liked_quizzes_num = len(liked_quizzes)
    #Correct_Wrong
    answered_quizzes = Quiz.objects.all().filter(answered_user=login_author)
    answered_quizzes_num = len(answered_quizzes)
    correct_quizzes = Quiz.objects.all().filter(first_try_correct=request.user)
    correct_quizzes_num = len(correct_quizzes)
    sliced_correct_quizzes = correct_quizzes[:5]
    wrong_quizzes = Quiz.objects.all().exclude(first_try_correct=request.user)
    wrong_quizzes_num = len(wrong_quizzes)
    sliced_wrong_quizzes = wrong_quizzes[:5]

    if not int(correct_quizzes_num ) == 0 and not int(answered_quizzes_num) == 0:
        correct_rate = "{:.0%}".format((int(correct_quizzes_num) / int(answered_quizzes_num)))
    else:
        correct_rate = 0
    #Article
    liked_articles = Articles.objects.all().filter(likes=request.user)
    sliced_liked_articles = liked_articles[:5]
    liked_articles_num = len(liked_articles)

    #Correction
    submitted_corrections = Correction.objects.all().filter(login_name=request.user)
    submitted_corrections_num = len(submitted_corrections)

    return render(request, 'quiz/register/user_detail.html', {
        'user': login_author,
        #Quiz
        'object_list': sliced_liked_quizzes,
        'liked_quizzes_num': liked_quizzes_num,
        'correct_quizzes':sliced_correct_quizzes,
        'correct_quizzes_num': correct_quizzes_num,
        'wrong_quizzes': sliced_wrong_quizzes,
        'wrong_quizzes_num': wrong_quizzes_num,
        'correct_rate': correct_rate,
        #Articles
        'liked_articles': sliced_liked_articles,
        'liked_articles_num': liked_articles_num,
        #Correction
        'submitted_corrections': submitted_corrections,
        'submitted_corrections_num': submitted_corrections_num,
    })

"""
def ActivitiesOfUser(request, pk):
    login_author = get_object_or_404(User, pk=pk)
    all_questions = Question.objects.all()
    questions = all_questions.filter(login_author=login_author)[:5]

    all_answers = Answer.objects.all()
    answers = all_answers.filter(login_author=login_author)[:5]

    return render(request, 'sensei_app/activities_of_user.html', {
        'user': login_author,
        'questions': questions,
        'answers': answers,
    })
"""

def AllQuizzesofUser(request, pk):
    login_author = get_object_or_404(User, pk=pk)
    all_questions = Quiz.objects.all()
    quizzes = all_questions.filter(likes=login_author)

    quizzes_of_user_query = request.GET.get('q')
    if quizzes_of_user_query:
        quizzes = quizzes.filter(
            Q(question__icontains=quizzes_of_user_query) |
            Q(choice1__icontains=quizzes_of_user_query) |
            Q(choice2__icontains=quizzes_of_user_query) |
            Q(choice3__icontains=quizzes_of_user_query) |
            Q(choice4__icontains=quizzes_of_user_query)
        ).distinct()

    quizzes = QuizFilter(
        request.GET,
        queryset=quizzes,
    )

    paginator = Paginator(quizzes.qs, 10)
    page_number = request.GET.get('page')
    quiz_page_obj = paginator.get_page(page_number)

    return render(request, 'quiz/quizzes/all_quizzes_of_user.html', {
        'login_user': login_author,
        'quizzes': quizzes,
        'quiz_page_obj': quiz_page_obj,
        'num': page_number,
        'paginator': paginator,
        'quizzes_of_user_query': 1,
     })

def CorrectQuizzesofUser(request,pk):
    login_author = get_object_or_404(User, pk=pk)
    correct_quizzes = Quiz.objects.all().filter(first_try_correct=request.user)


    quizzes_of_user_query = request.GET.get('q')
    if quizzes_of_user_query:
        correct_quizzes = correct_quizzes.filter(
            Q(question__icontains=quizzes_of_user_query) |
            Q(choice1__icontains=quizzes_of_user_query) |
            Q(choice2__icontains=quizzes_of_user_query) |
            Q(choice3__icontains=quizzes_of_user_query) |
            Q(choice4__icontains=quizzes_of_user_query)
        ).distinct()

    correct_quizzes = QuizFilter(
        request.GET,
        queryset=correct_quizzes,
    )

    paginator = Paginator(correct_quizzes.qs, 10)
    page_number = request.GET.get('page')
    quiz_page_obj = paginator.get_page(page_number)

    return render(request, 'quiz/quizzes/correct_quizzes_of_user.html', {
        'login_user': login_author,
        'quizzes': correct_quizzes,
        'correct_quizzes': 1,
        'quiz_page_obj': quiz_page_obj,
        'num': page_number,
        'paginator': paginator,
        'quizzes_of_user_query': 1,
     })

def WrongQuizzesofUser(request,pk):
    login_author = get_object_or_404(User, pk=pk)
    wrong_quizzes = Quiz.objects.all().exclude(first_try_correct=request.user)

    quizzes_of_user_query = request.GET.get('q')
    if quizzes_of_user_query:
        correct_quizzes = wrong_quizzes.filter(
            Q(question__icontains=quizzes_of_user_query) |
            Q(choice1__icontains=quizzes_of_user_query) |
            Q(choice2__icontains=quizzes_of_user_query) |
            Q(choice3__icontains=quizzes_of_user_query) |
            Q(choice4__icontains=quizzes_of_user_query)
        ).distinct()

    wrong_quizzes = QuizFilter(
        request.GET,
        queryset=wrong_quizzes,
    )

    paginator = Paginator(wrong_quizzes.qs, 10)
    page_number = request.GET.get('page')
    quiz_page_obj = paginator.get_page(page_number)

    return render(request, 'quiz/quizzes/wrong_quizzes_of_user.html', {
        'login_user': login_author,
        'quizzes': wrong_quizzes,
        'wrong_quizzes': 1,
        'quiz_page_obj': quiz_page_obj,
        'num': page_number,
        'paginator': paginator,
        'quizzes_of_user_query': 1,
    })

def AllArticlesofUser(request, pk):
    login_author = get_object_or_404(User, pk=pk)

    all_articles = Articles.objects.all()
    articles = all_articles.filter(likes=login_author)

    answers_of_user_query = request.GET.get('q')
    if answers_of_user_query:
        articles = articles.filter(
            Q(title__icontains=answers_of_user_query) |
            Q(content__icontains=answers_of_user_query)
        ).distinct()

    paginator = Paginator(articles, 10)
    page_number = request.GET.get('page')
    article_page_obj = paginator.get_page(page_number)

    return render(request, 'quiz/articles/all_articles_of_user.html', {
        'login_user': login_author,
        'articles': articles,
        'article_list': article_page_obj,
        'num': page_number,
        'paginator':paginator,
        'answer_of_user_query': 1,
    })

class UserUpdate(OnlyYouMixin, generic.UpdateView):
    """ユーザー情報更新ページ"""
    model = User
    form_class = UserUpdateForm
    template_name = 'quiz/register/user_update.html'  # デフォルトユーザーを使う場合に備え、きちんとtemplate名を書く

    def get_success_url(self):
        return resolve_url('quiz:user_detail', pk=self.kwargs['pk'])


class PasswordChange(PasswordChangeView):
    """パスワード変更ビュー"""
    form_class = MyPasswordChangeForm
    success_url = reverse_lazy('quiz:password_change_done')
    template_name = 'quiz/register/password_change.html'


class PasswordChangeDone(PasswordChangeDoneView):
    """パスワード変更しました"""
    template_name = 'quiz/register/password_change_done.html'


class PasswordReset(PasswordResetView):
    """パスワード変更用URLの送付ページ"""
    subject_template_name = 'quiz/mail_template/password_reset/subject.txt'
    email_template_name = 'quiz/mail_template/password_reset/message.txt'
    template_name = 'quiz/register/password_reset_form.html'
    form_class = MyPasswordResetForm
    success_url = reverse_lazy('quiz:password_reset_done')


class PasswordResetDone(PasswordResetDoneView):
    """パスワード変更用URLを送りましたページ"""
    template_name = 'quiz/register/password_reset_done.html'


class PasswordResetConfirm(PasswordResetConfirmView):
    """新パスワード入力ページ"""
    form_class = MySetPasswordForm
    success_url = reverse_lazy('quiz:password_reset_complete')
    template_name = 'quiz/register/password_reset_confirm.html'


class PasswordResetComplete(PasswordResetCompleteView):
    """新パスワード設定しましたページ"""
    template_name = 'quiz/register/password_reset_complete.html'


class EmailChange(LoginRequiredMixin, generic.FormView):
    """メールアドレスの変更"""
    template_name = 'quiz/register/email_change_form.html'
    form_class = EmailChangeForm

    def form_valid(self, form):
        user = self.request.user
        new_email = form.cleaned_data['email']

        # URLの送付
        current_site = get_current_site(self.request)
        domain = current_site.domain

        context = {
            'protocol': 'https' if self.request.is_secure() else 'http',
            'domain': domain,
            'token': dumps(new_email),
            'user': user,
        }

        subject = render_to_string('quiz/mail_template/email_change/subject.txt', context)
        subject = subject.strip()
        message = render_to_string('quiz/mail_template/email_change/message.txt', context)
        send_mail(subject, message, None, [new_email])

        return redirect('quiz:email_change_done')


class EmailChangeDone(LoginRequiredMixin, generic.TemplateView):
    """メールアドレスの変更メールを送ったよ"""
    template_name = 'quiz/register/email_change_done.html'


class EmailChangeComplete(LoginRequiredMixin, generic.TemplateView):
    """リンクを踏んだ後に呼ばれるメアド変更ビュー"""
    template_name = 'quiz/register/email_change_complete.html'
    timeout_seconds = getattr(settings, 'ACTIVATION_TIMEOUT_SECONDS', 60 * 60 * 24)  # デフォルトでは1日以内

    def get(self, request, **kwargs):
        token = kwargs.get('token')
        try:
            new_email = loads(token, max_age=self.timeout_seconds)

        # 期限切れ
        except SignatureExpired:
            return HttpResponseBadRequest()

        # tokenが間違っている
        except BadSignature:
            return HttpResponseBadRequest()

        # tokenは問題なし
        else:
            User.objects.filter(email=new_email, is_active=False).delete()
            request.user.email = new_email
            request.user.save()
            return super().get(request, **kwargs)
