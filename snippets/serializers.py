# _*_ coding:UTF-8 _*_
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import *


class SnippetSerializer(serializers.ModelSerializer):
    #pk = Serializer.IntegerField()
    #title = serializers.CharField(required=False,max_length=100)
    #code = serializers.CharField(max_length=100000)
    #linenos = serializers.BooleanField(required=False)
    #language = serializers.ChoiceField(choices = LANGUAGE_CHOICES,default='python')
    #style = serializers.ChoiceField(choices=STYLE_CHOICES,default='friendly')

    # def restore_object(self,attrs,instance=None):
    #   if instance:
    #       instance.title = attrs.get('title',instance.title)
    #       instance.code = attrs.get('code',instance.code)
    #       instance.linenos = attrs.get('linenos',instance.linenos)
    #       instance.language = attrs.get('language',instance.language)
    #       instance.style = attrs.get('style',instance.style)
    #       return instance
    #   return Snippet(**attrs)

    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Snippet
        fields = ('id', 'title', 'code', 'linenos',
                  'language', 'style', 'owner')


class UserSerializer(serializers.ModelSerializer):
    snippets = serializers.HyperlinkedRelatedField(
        many=True, read_only=True, view_name='snippet-detail')
    #snippets = SnippetSerializer(many=True,read_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'snippets')
