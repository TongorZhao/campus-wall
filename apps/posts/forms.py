from django import forms
from django.utils.text import slugify
from .models import Post, PostImage, Tag


class PostForm(forms.ModelForm):
    tags_input = forms.CharField(
        required=False,
        label='标签',
        help_text='多个标签用逗号分隔',
        widget=forms.TextInput(attrs={'placeholder': '例如：表白, 寻物, 二手'}),
    )

    class Meta:
        model = Post
        fields = ('title', 'content', 'category', 'anonymity')
        widgets = {
            'content': forms.Textarea(attrs={'rows': 8}),
        }


class PostImageForm(forms.ModelForm):
    class Meta:
        model = PostImage
        fields = ('image',)


PostImageFormSet = forms.inlineformset_factory(
    Post,
    PostImage,
    form=PostImageForm,
    extra=4,
    max_num=9,
    can_delete=False,
)


class CommentForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('content',)
        widgets = {
            'content': forms.Textarea(attrs={
                'rows': 3,
                'placeholder': '写下你的评论...',
            }),
        }


class SearchForm(forms.Form):
    q = forms.CharField(
        required=True,
        label='搜索',
        widget=forms.TextInput(attrs={
            'placeholder': '搜索帖子...',
            'autofocus': True,
        }),
    )
    category = forms.CharField(required=False, widget=forms.HiddenInput())
