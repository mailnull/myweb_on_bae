# _*_ coding:UTF-8 _*_
import sys
reload(sys)
sys.setdefaultencoding('utf8')
from django.db import models
from django.utils.html import format_html
from django.contrib import admin
from datetime import datetime
from django.contrib.auth.models import User
import time
import datetime

# Create your models here.


class Author(models.Model):
    authorType = (
        (None, u"账号类型"),
        (0, u"订阅号"),
        (1, u"服务号"),
        (2, u"认证订阅号"),
        (3, u"认证服务号"),
        (4, u"测试号"),
    )
    author = models.CharField(u"公众号openid", max_length=20, unique=True)
    nickname = models.CharField(u"公众号昵称", max_length=16, blank=True, null=True)
    author_type = models.SmallIntegerField(
        u'公众号类型', choices=authorType, default=0, help_text=u"0:订阅号 1:服务号 2:认证订阅号 3:认证服务号 4:测试号")

    def __unicode__(self):
        return u"%s" % (self.get_author_type_display())

    class Meta:
        verbose_name = u"公众号表"
        verbose_name_plural = u"公众号表"


class WeiUser(models.Model):
    openid = models.CharField(u"用户openid", max_length=32, unique=True)
    author = models.ForeignKey(
        Author, verbose_name=u"公众号", blank=True, null=True, on_delete=models.SET_NULL)
    subscribe_time = models.IntegerField(u"关注时间", default=0)
    unsubscribe_time = models.IntegerField(u"取消关注时间", blank=True, null=True)
    subscribe = models.BooleanField(u"关注", default=False)
    nickname = models.CharField(u"昵称", max_length=12, blank=True, null=True)

    def __unicode__(self):
        return u"%s|%s" % (self.openid, self.nickname)

    class Meta:
        verbose_name = u'公众号用户表'
        verbose_name_plural = u'公众号用户表'

# 用户消息


class Messges(models.Model):
    user = models.ForeignKey(WeiUser, verbose_name=u"用户",
                             blank=True, null=True, on_delete=models.SET_NULL)
    author = models.ForeignKey(
        Author, verbose_name=u"公众号", blank=True, null=True, on_delete=models.SET_NULL)
    CreateTime = models.IntegerField(u"接收时间")
    MsgType = models.CharField(u"消息类型", max_length=10)
    MsgId = models.BigIntegerField(u"消息ID", blank=True, null=True)
    Content = models.TextField(u"消息", blank=True, null=True)
    PicUrl = models.URLField(u"图片链接", blank=True, null=True)
    MediaId = models.CharField(u"媒体消息ID", max_length=65, blank=True, null=True)
    Format = models.CharField(u"语音格式", max_length=8, blank=True, null=True)
    Recognition = models.CharField(
        u"语音识别", max_length=20, blank=True, null=True)
    ThumbMediaId = models.CharField(
        u"视频缩略图", max_length=65, blank=True, null=True)
    Location_X = models.FloatField(u"纬度", blank=True, null=True)
    Location_Y = models.FloatField(u"经度", blank=True, null=True)
    Label = models.CharField(u"地理位置信息", max_length=50, blank=True, null=True)
    Scale = models.SmallIntegerField(u"地理位置缩放", blank=True, null=True)
    Title = models.CharField(u"消息标题", max_length=100, blank=True, null=True)
    Description = models.TextField(u"消息描述", blank=True, null=True)
    Url = models.URLField(u"消息链接", blank=True, null=True)
    Event = models.CharField(u"事件类型", max_length=12, blank=True, null=True)
    EventKey = models.CharField(
        u"事件KEY值", max_length=64, blank=True, null=True)
    Ticket = models.CharField(
        u"二维码的ticket", max_length=64, blank=True, null=True)

    def __unicode__(self):
        return u"%s|%s" % (self.user, self.MsgId)

    def selectdisply(self):
        display = ""
        if self.MsgType == "text":
            display = "MsgId=%s|Content=%s" % (self.MsgId, self.Content)
        elif self.MsgType == "event":
            display = "Event=%s|EventKey=%s" % (self.Event, self.EventKey)
        elif self.MsgType == "image":
            # PicUrl=format_html('<a href="{}" title="{}">查看图片</a>',
            # self.PicUrl,
            # self.PicUrl)
            display = "MsgId=%s|PicUrl=%s|MediaId=%s" % (self.MsgId, format_html('<a href="{}" title="{}">查看图片</a>',
                                                                                 self.PicUrl,
                                                                                 self.PicUrl), self.MediaId)
        elif self.MsgType == "voice":
            display = "MsgId=%s|MediaId=%s|Recognition=%s" % (
                self.MsgId, self.MediaId, self.Recognition)
        elif self.MsgType == "link":
            display = "MsgId=%s|Title=%s|Url=%s|Description=$s" % (
                self.MsgId, self.Title, self.Url, self.Description)
        elif self.MsgType == "location":
            display = u"MsgId=%s|Location_X=%f|Location_Y=%f" % (
                self.MsgId, self.Location_X, self.Location_Y)
        else:
            display = ["MsgId"]
        return display
    selectdisply.allow_tags = True
    selectdisply.short_description = u"消息简介"

    class Meta:
        verbose_name = u"消息表"
        verbose_name_plural = u"消息表"
        ordering = ['user', '-CreateTime']


# 用户上报的地理位置
class Location(models.Model):
    user = models.ForeignKey(WeiUser, verbose_name=u"用户",
                             blank=True, null=True, on_delete=models.SET_NULL)
    Latitude = models.FloatField(u"上报的纬度", blank=True, null=True)
    Longitude = models.FloatField(u"上报的经度", blank=True, null=True)
    Precision = models.FloatField(u"地理位置精度", blank=True, null=True)
    CreateTime = models.IntegerField(u"接收时间")

    def __unicode__(self):
        return u"%s" % (user)

    class Meta:
        verbose_name = u"地理位置"
        verbose_name_plural = u"地理位置"
        ordering = ['user', '-CreateTime']


class Cachelast(models.Model):
    user = models.ForeignKey(WeiUser, verbose_name=u"用户",
                             blank=True, null=True, on_delete=models.SET_NULL)
    MsgId = models.BigIntegerField(blank=True, null=True)
    CreateTime = models.IntegerField()

    def __unicode__(self):
        return u"%s|%s|%s" % (self.user, self, CreateTime, self.MsgId)


# datetime.fromtimestamp(time.time())

# class Article(models.Model):
#   caption = models.CharField(u"标题",max_length=30)
#   author = models.ForeignKey(Author,verbose_name = "作者")
#   content = models.TextField(u"正文")
#   tags = models.ManyToManyField(Tag)
#   category = models.ForeignKey(Category)
#   click = models.IntegerField(default=0)
#   created_date = models.DateTimeField(u"发布时间",auto_now_add = True)
#   publish_date = models.DateTimeField(u"修改时间",blank = True,null=True)


#   def publish(self):
#       self.publish_date=datetime.now()
#       self.save()
#   def __unicode__(self):
#       return u"%s"%(self.caption)
#   #显示样式
#   def shortdisplay(self):
#       if self.content:
#           return format_html('<span style="color:red">{}</span>',
#               u'%s'%(self.content[:100]))
#       else:
#           return u""
#   shortdisplay.allow_tags = True
#   shortdisplay.short_description=u"博客正文"
#   class Meta:
#       ordering=['-created_date']
#       verbose_name = u'博客'
#       verbose_name_plural = u'博客'

# class ArticleAdmin(admin.ModelAdmin):
#   list_display=('caption','author','created_date','shortdisplay')

# 微信access_token
class Access_token(models.Model):
    author = models.OneToOneField(
        Author, verbose_name=u"公众号", blank=True, null=True, on_delete=models.SET_NULL)
    access_token = models.CharField(
        u"access_token", max_length=140, blank=True, null=True)
    expires_in = models.IntegerField(u"expires_in")

    def __unicode__(self):
        return "{0}::{1}".format(self.author, self.access_token)

    class Meta:
        verbose_name = u'微信_access_token'
        verbose_name_plural = u'微信_access_token'

    def time_to_date(self):
        if self.expires_in:
            return datetime.datetime.fromtimestamp(self.expires_in)
        else:
            return None
    time_to_date.short_description = u"expires_in"

# 百度access_token


class Baidu_author(models.Model):
    author = models.CharField(u'百度用户', max_length=16)
    App_ID = models.PositiveIntegerField(
        u'App ID', default=None, unique=True)
    API_Key = models.CharField(u'API Key', max_length=30)
    Secret_Key = models.CharField(u'Secret Key', max_length=50)

    class Meta:
        verbose_name = u"百度用户"
        verbose_name_plural = u"百度用户"

    def __unicode__(self):
        return '%s' % (self.author)


class Baidu_access_token(models.Model):
    author = models.ForeignKey(
        Baidu_author, verbose_name=u'百度用户', blank=True, null=True, on_delete=models.SET_NULL)
    App_ID = models.PositiveIntegerField(u'App_ID', blank=True, null=True)
    access_token = models.CharField(
        u'access_token', max_length=100, blank=True, null=True)
    expires_in = models.IntegerField(u'expires_in', blank=True, null=True)

    class Meta:
        verbose_name = "Baidu_access_token"
        verbose_name_plural = "Baidu_access_tokens"

    def __unicode__(self):
        return '{0}::{1}'.format(self.access_token, self.expires_in)

    def time_to_date(self):
        if self.expires_in:
            return datetime.datetime.fromtimestamp(self.expires_in)
        else:
            return None
    time_to_date.short_description = u'expires_in'
