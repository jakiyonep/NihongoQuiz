from django.contrib import admin
from quiz.models import Category, Tag, Quiz
# Register your models here.


admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(Quiz)