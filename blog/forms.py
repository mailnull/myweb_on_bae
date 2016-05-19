# _*_ coding:UTF-8 _*
from django import forms
from .models import *

class PostForm(forms.ModelForm):

    class Meta:
        model = Article
        fields = ('caption', 'content','category')
        labels = {
        	'category': '分类目录',
        	'content': '正文',
        	'caption': '标题',
        }
        widgets = {
        	'content': forms.Textarea(attrs={'rows': 15}),
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('author', 'email', 'text')
        labels = {
            'author': '昵称(必填)',
            'email': '电子邮箱(我们会为您保密)(必填)',
            'text': '评论内容',
        }
        widgets = {
            'text': forms.Textarea(attrs={'rows': 7}),
        }