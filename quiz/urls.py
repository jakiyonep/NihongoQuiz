from django.urls import path
from quiz.views import (
    Index,
    LevelListView,
    CategoryListView,
    TagListView,
    LevelPostView,
    CategoryPostView,
    TagPostView,
    SearchPostView,
    QuizFilter,
)


app_name = 'quiz'

urlpatterns = [
    path('', Index.as_view(), name='index'),
    path('levels/', LevelListView.as_view(), name="level_list"),
    path('categories/', CategoryListView.as_view(), name="category_list"),
    path('tags/', TagListView.as_view(), name="tag_list"),
    path('level/<str:level_slug>/', LevelPostView.as_view(), name ="level_post"),
    path('category/<str:category_slug>/', CategoryPostView.as_view(), name ="category_post"),
    path('tag/<str:tag_slug>/', TagPostView.as_view(), name ="tag_post"),
    path('search/', SearchPostView.as_view(), name='search_post'),

]