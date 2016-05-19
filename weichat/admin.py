from django.contrib import admin
from .models import *


# Register your models here.

class AuthorAdmin(admin.ModelAdmin):
    list_display = ["author", "nickname", "author_type"]


class WeiUserAdmin(admin.ModelAdmin):
    list_display = ["openid", "author", "nickname",
                    "subscribe", "subscribe_time", "unsubscribe_time"]


class MessgesAdmin(admin.ModelAdmin):
    list_display = ["user", "author", "CreateTime", "MsgType", "selectdisply"]


class LocationAdmin(admin.ModelAdmin):
    list_display = ["user", "CreateTime", "Latitude", "Longitude"]


class CachelastAdmin(admin.ModelAdmin):
    list_display = ["user", "MsgId", "CreateTime"]


class Access_tokenAdmin(admin.ModelAdmin):
    list_display = ['author', 'access_token', 'time_to_date']


class Baidu_authorAdmin(admin.ModelAdmin):
    list_display = ['author','App_ID', 'API_Key', 'Secret_Key']


class Baidu_access_tokenAdmin(admin.ModelAdmin):
    list_display = ['author', 'App_ID','access_token', 'time_to_date']

admin.site.register(Author, AuthorAdmin)
admin.site.register(WeiUser, WeiUserAdmin)
admin.site.register(Messges, MessgesAdmin)
admin.site.register(Location, LocationAdmin)
admin.site.register(Cachelast, CachelastAdmin)
admin.site.register(Access_token, Access_tokenAdmin)
admin.site.register(Baidu_author, Baidu_authorAdmin)
admin.site.register(Baidu_access_token, Baidu_access_tokenAdmin)
