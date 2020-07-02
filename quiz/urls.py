from django.urls import path
from quiz.views import *


app_name = 'quiz'

urlpatterns = [
    path('', ToppageView.as_view(), name="toppage"),
    path('beforeyoustart', BeforeYouStart.as_view(), name='before_you_start'),
    path('quiz', QuizListView, name='quiz'),
    path('level/<str:level_slug>/', LevelPostView.as_view(), name ="level_post"),
    path('category/<str:category_slug>/', CategoryPostView.as_view(), name ="category_post"),
    path('tag/<str:tag_slug>/', TagPostView.as_view(), name ="tag_post"),
    path('search/', SearchPostView.as_view(), name='search_post'),
    path('basics/', BasicsIndex.as_view(), name="basics"),
    path('basic/<str:title_slug>/', BasicsDetailView.as_view(), name="basic_post"),
    path('advanced/', ArticlesIndex.as_view(), name="articles"),
    path('advanced/<str:title_slug>/', ArticleDetailView.as_view(), name="article_post"),
    path('advanced/tag/<str:article_tag_slug>/', ArticleTagsView.as_view(), name='article_tag_post'),
    path('lessons/', LessonsIndex.as_view(), name="lessons"),
    path('lesson/<str:pk>/', LessonDetailView.as_view(), name="lesson_post"),
    path('lessonvocabulary/', LessonVocabularyIndex.as_view(), name="lesson_vocabulary"),
    path('lessongrammar/', LessonGrammarIndex.as_view(), name="lesson_grammar"),
    path('lessonkanji/', LessonKanjiIndex.as_view(), name="lesson_kanji"),
    path('correction/', CorrectionIndex.as_view(), name="correction"),
    path('correctionadd/', CorrectionAdd, name="correction_add"),
    path('submitted', AfterSubmit, name="after_submit"),
    path('correction/<str:title_slug>/', CorrectionDetail.as_view(), name="correction_post")
]