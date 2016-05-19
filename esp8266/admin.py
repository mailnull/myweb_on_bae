# _*_ coding:UTF-8 _*_
from django.contrib import admin
from .models import *
from django.utils.html import format_html
# Register your models here.


class DeviceAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_date')


class PostsAdmin(admin.ModelAdmin):
    list_display = ('device', 'temp', 'published_date')


class TestfileAdmin(admin.ModelAdmin):
    list_display = ['title', 'dateform','url']

    def url(self,obj):
        #return format_html('<img src="/media{}">',obj.get_absolute_url())
        return format_html('<a href="/media{}" title="{}">查看图片</a>',obj.get_absolute_url(),obj.title)


admin.site.register(Device, DeviceAdmin)
admin.site.register(Posts, PostsAdmin)
admin.site.register(Testfile, TestfileAdmin)
