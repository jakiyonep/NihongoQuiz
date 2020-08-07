from django.urls import path
from quiz.views import *
from . import views

app_name = 'quiz'

urlpatterns = [
    path('', ToppageView.as_view(), name="toppage"),
    path('beforeyoustart', BeforeYouStart.as_view(), name='before_you_start'),
    path('quiz', QuizListView, name='quiz'),
    path('quiz/level/<str:level_slug>/', LevelPost, name ="level_post"),
    path('quiz/category/<str:category_slug>/', CategoryPost, name ="category_post"),
    path('quiz/tag/<str:tag_slug>/', TagPost, name ="tag_post"),
    path('quiz/search/', QuizSearchList, name='search_post'),
    path('quiz/like', views.QuizLike, name='quiz_like'),
    path('quiz/choice', views.QuizPoll, name='quiz_choice'),

    path('basics/', BasicsIndex.as_view(), name="basics"),
    path('basic/<str:title_slug>/', BasicsDetailView.as_view(), name="basic_post"),

    path('articles/', ArticleList, name="articles"),
    path('article/<str:title_slug>/', ArticleDetail, name="article_post"),
    path('articles/tag/<str:article_tag_slug>/', ArticleTagsView, name='article_tag_post'),
    path('articles/category/<str:article_category2_slug>/', ArticleCategoryView, name="article_category_post"),
    path('article/like', views.ArticleLike, name='article_like'),

    path('comment/add', views.CommentAdd, name='comment_add'),
    path('comment/<int:pk>/approve/', comment_approve, name='comment_approve'),
    path('comment/<int:pk>/remove/', comment_remove, name='comment_remove'),
    path('reply/add', views.ReplyAdd, name='reply_add'),
    path('reply/<int:pk>/approve/', reply_approve, name='reply_approve'),
    path('reply/<int:pk>/remove/', reply_remove, name='reply_remove'),

    path('lessons/', LessonsIndex.as_view(), name="lessons"),
    path('lesson/<str:pk>/', LessonDetailView.as_view(), name="lesson_post"),
    path('lessonvocabulary/', LessonVocabularyIndex.as_view(), name="lesson_vocabulary"),
    path('lessongrammar/', LessonGrammarIndex.as_view(), name="lesson_grammar"),
    path('lessonkanji/', LessonKanjiIndex.as_view(), name="lesson_kanji"),

    path('correction/', CorrectionIndex.as_view(), name="correction"),
    path('correction/add/', CorrectionAdd, name="correction_add"),
    path('submitted', AfterSubmit, name="after_submit"),
    path('correction/<str:title_slug>/', CorrectionDetail.as_view(), name="correction_post"),

    path('login/', views.Login.as_view(), name='login'),
    path('logout/', views.Logout.as_view(), name='logout'),
    path('user_create/', views.UserCreate.as_view(), name='user_create'),
    path('user_create/done/', views.UserCreateDone.as_view(), name='user_create_done'),
    path('user_create/complete/<token>/', views.UserCreateComplete.as_view(), name='user_create_complete'),
    path('user_detail/<int:pk>/', views.UserDetail, name='user_detail'),
    path('user_detail/<int:pk>/questions', AllQuizzesofUser, name="all_quizzes_of_user"),
    path('user_detail/<int:pk>/articles', AllArticlesofUser, name='all_articles_of_user'),
    path('user_detail/<int:pk>/questions/correct', CorrectQuizzesofUser, name="correct_quizzes_of_user"),
    path('user_detail/<int:pk>/questions/wrong', WrongQuizzesofUser, name="wrong_quizzes_of_user"),
    #path('user_detail/<int:pk>/question_list', ActivitiesOfUser, name='activities_of_user'),
    path('user_update/<int:pk>/', views.UserUpdate.as_view(), name='user_update'),
    path('password_change/', views.PasswordChange.as_view(), name='password_change'),
    path('password_change/done/', views.PasswordChangeDone.as_view(), name='password_change_done'),
    path('password_reset/', views.PasswordReset.as_view(), name='password_reset'),
    path('password_reset/done/', views.PasswordResetDone.as_view(), name='password_reset_done'),
    path('password_reset/confirm/<uidb64>/<token>/', views.PasswordResetConfirm.as_view(),
         name='password_reset_confirm'),
    path('password_reset/complete/', views.PasswordResetComplete.as_view(), name='password_reset_complete'),
    path('email/change/', views.EmailChange.as_view(), name='email_change'),
    path('email/change/done/', views.EmailChangeDone.as_view(), name='email_change_done'),
    path('email/change/complete/<str:token>/', views.EmailChangeComplete.as_view(), name='email_change_complete'),
]