from django import forms
from django.forms import ModelForm, TextInput, Textarea, Select
from .models import Correction, Comment, Reply
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class CorrectionForm(forms.ModelForm):
    class Meta():
        model = Correction
        fields = ('name', 'type', 'text', 'desc')
        widgets = {
            'name': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Name',
            }),
            'type': Select(attrs={
                'class': 'form-control',
                'placeholder': 'Type',
            }),
            'login_author': forms.HiddenInput(),
            'text': Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Text',
            }),
            'desc': Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Description',
            })
        }

class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ('author','login_author', 'text', 'aki')
        widgets = {
            'author': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Name',
            }),
            'login_author': forms.HiddenInput(),
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
        fields = ('author','login_author', 'text', 'aki')
        widgets = {
            'author': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Name',
            }),
            'login_author': forms.HiddenInput(),
            'text': Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Reply',
            }),
        }
        labels = {
            'author': '',
            'text': '',
        }

#USER REGISTRATION

from django.contrib.auth.forms import (
    AuthenticationForm, UserCreationForm, PasswordChangeForm,
    PasswordResetForm, SetPasswordForm
)
from django.contrib.auth import get_user_model

User = get_user_model()

class EmailChangeForm(forms.ModelForm):
    """メールアドレス変更フォーム"""

    class Meta:
        model = User
        fields = ('email',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

    def clean_email(self):
        email = self.cleaned_data['email']
        User.objects.filter(email=email, is_active=False).delete()
        return email

class LoginForm(AuthenticationForm):
    """ログインフォーム"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['placeholder'] = field.label  # placeholderにフィールドのラベルを入れる

class UserCreateForm(UserCreationForm):
    """ユーザー登録用フォーム"""

    class Meta:
        model = User
        fields = ('email', 'nickname',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

    def clean_email(self):
        email = self.cleaned_data['email']
        User.objects.filter(email=email, is_active=False).delete()
        return email

class UserUpdateForm(forms.ModelForm):
    """ユーザー情報更新フォーム"""

    class Meta:
        model = User
        fields = ('nickname',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

class   MyPasswordChangeForm(PasswordChangeForm):
    """パスワード変更フォーム"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

class MyPasswordResetForm(PasswordResetForm):
    """パスワード忘れたときのフォーム"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

class MySetPasswordForm(SetPasswordForm):
    """パスワード再設定用フォーム(パスワード忘れて再設定)"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'