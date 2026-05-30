from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True, label='邮箱')
    nickname = forms.CharField(max_length=30, required=True, label='昵称')
    school = forms.CharField(max_length=100, required=False, label='学校')

    class Meta:
        model = User
        fields = ('username', 'nickname', 'email', 'school', 'password1', 'password2')


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('nickname', 'avatar', 'bio', 'school', 'grade', 'phone')
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 4}),
        }
