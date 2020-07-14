from django import forms
from django.forms import ModelForm, TextInput, Textarea
from .models import Correction, Comment, Reply


class CorrectionForm(forms.ModelForm):
    class Meta():
        model = Correction
        fields = ('name', 'type', 'text', 'desc')


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ('author', 'text', 'aki')
        widgets = {
            'author': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Name',
            }),
            'text': Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Comment',
            }),
        }
        labels = {
            'author': '',
            'text': '',
        }


class ReplyForm(ModelForm):
    class Meta:
        model = Reply
        fields = ('author', 'text', 'aki')
        widgets = {
            'author': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Name',
            }),
            'text': Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Reply',
            }),
        }
        labels = {
            'author': '',
            'text': '',
        }

