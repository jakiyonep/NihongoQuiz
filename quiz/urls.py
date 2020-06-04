from django.urls import path
from quiz.views import (
    QuizListView,
    LevelListView,
    CategoryListView,
    TagListView,
    LevelPostView,
    CategoryPostView,
    TagPostView,
    SearchPostView,
    QuizFilter,
    BasicsDetailView,
    BasicsIndex,
    ToppageView,
    LessonsIndex,
    LessonDetailView,
)


app_name = 'quiz'

urlpatterns = [
    path('', ToppageView.as_view(), name="toppage"),
    path('quiz', QuizListView.as_view(), name='quiz'),
    path('levels/', LevelListView.as_view(), name="level_list"),
    path('categories/', CategoryListView.as_view(), name="category_list"),
    path('tags/', TagListView.as_view(), name="tag_list"),
    path('level/<str:level_slug>/', LevelPostView.as_view(), name ="level_post"),
    path('category/<str:category_slug>/', CategoryPostView.as_view(), name ="category_post"),
    path('tag/<str:tag_slug>/', TagPostView.as_view(), name ="tag_post"),
    path('search/', SearchPostView.as_view(), name='search_post'),
    path('basics/', BasicsIndex.as_view(), name="basics"),
    path('basic/<str:pk>/', BasicsDetailView.as_view(), name="basic_post"),
    path('lessons/', LessonsIndex.as_view(), name="lessons"),
    path('lesson/<str:pk>/', LessonDetailView.as_view(), name="lesson_post"),

]