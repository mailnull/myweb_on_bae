# _*_ coding:UTF-8 _*_
from .models import *
from rest_framework import serializers
		
class WeiUserSerializer(serializers.ModelSerializer):
	#msgs = serializers.HyperlinkedIdentityField('messges', view_name='messges-detail', lookup_field='user')
	class Meta:
		model = WeiUser,
		#fields = ('openid','nickname','msgs')

class MessagesSerializer(serializers.ModelSerializer):
	#user = WeiUserSerializer(required = True)

	user = serializers.ReadOnlyField(source='user.nickname')
	class Meta:
		model = Messges

