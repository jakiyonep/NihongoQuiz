from django.urls import path
from quiz.views import Index, CategoryListView, TagListView, QuizDetailView

app_name = 'quiz'

urlpatterns = [
    path('', Index.as_view(), name='index'),
    path('quiz/<int:pk>', QuizDetailView.as_view(), name="quiz_detail"),
    path('categories/', CategoryListView.as_view(), name="category_list"),
    path('tags/', TagListView.as_view(), name="tag_list"),
]