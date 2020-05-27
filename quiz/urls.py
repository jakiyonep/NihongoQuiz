from django.urls import path
from quiz.views import (
    Index,
    CategoryListView,
    TagListView,
    QuizDetailView,
    CategoryPostView,
    TagPostView,
)


app_name = 'quiz'

urlpatterns = [
    path('', Index.as_view(), name='index'),
    path('quiz/<int:pk>', QuizDetailView.as_view(), name="quiz_detail"),
    path('categories/', CategoryListView.as_view(), name="category_list"),
    path('tags/', TagListView.as_view(), name="tag_list"),
    path('category/<str:category_slug>/', CategoryPostView.as_view(), name ="category_post"),
    path('tag/<str:tag_slug>/', TagPostView.as_view(), name ="tag_post")
]