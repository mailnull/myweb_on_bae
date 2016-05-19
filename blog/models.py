# _*_ coding:UTF-8 _*_
import sys
reload(sys)
sys.setdefaultencoding('utf8')
from django.db import models
from django.utils.html import format_html
from django.contrib import admin
from datetime import datetime
from django.contrib.auth.models import User


class esptemp(models.Model):
    device = models.CharField(max_length=10, unique=True)
    temp = models.CharField(max_length=8, default="0", unique=True)

    def __unicode__(self):
        return self.device


class esptempAdmin(admin.ModelAdmin):
    list_display = ('device', 'temp')


class Tag(models.Model):

    class Meta:
        verbose_name = u'标签'
        verbose_name_plural = u'标签'

    name = models.CharField(max_length=40)

    def __str__(self):
        return self.name


class Category(models.Model):

    class Meta:
        verbose_name = u'分类目录'
        verbose_name_plural = u'分类目录'

    name = models.CharField(max_length=40)

    def __str__(self):
        return self.name


# 作者信息模型
class Author(models.Model):
    user = models.OneToOneField(User, verbose_name="作者")
    #name = models.CharField(u"作者",max_length=30)
    #email = models.EmailField(u"电子邮件",blank=True)
    nickname = models.CharField(u"昵称", max_length=10, blank=True)
    website = models.URLField(u"网站", blank=True)

    def __unicode__(self):
        return u"%s" % (self.user)

    def redandlinks(self):
        return format_html('<a href="{}" title="访问网站">{}</a>',
                           self.website,
                           self.website)
    redandlinks.allow_tags = True
    redandlinks.short_description = u'作者网站'

    class Meta:
        verbose_name = u'作者信息'
        verbose_name_plural = u'作者信息'

# 作者信息排列


class AuthorAdmin(admin.ModelAdmin):
    list_display = ('user', 'nickname', 'redandlinks')


class Article(models.Model):
    caption = models.CharField(u"标题", max_length=30)
    author = models.ForeignKey(Author, verbose_name="作者")
    content = models.TextField(u"正文")
    tags = models.ManyToManyField(Tag)
    category = models.ForeignKey(Category)
    click = models.IntegerField(default=0)
    created_date = models.DateTimeField(u"发布时间", auto_now_add=True)
    publish_date = models.DateTimeField(u"修改时间", blank=True, null=True)

    def publish(self):
        self.publish_date = datetime.now()
        self.save()

    def __unicode__(self):
        return u"%s" % (self.caption)
    # 显示样式

    def shortdisplay(self):
        if self.content:
            return format_html('<span style="color:red">{}</span>',
                               u'%s' % (self.content[:100]))
        else:
            return u""
    shortdisplay.allow_tags = True
    shortdisplay.short_description = u"博客正文"

    class Meta:
        ordering = ['-created_date']
        verbose_name = u'博客'
        verbose_name_plural = u'博客'


class ArticleAdmin(admin.ModelAdmin):
    list_display = ('caption', 'author', 'created_date', 'shortdisplay')


class Comment(models.Model):

    class Meta:
        verbose_name = u'评论'
        verbose_name_plural = u'评论'
    author = models.CharField(max_length=20)
    email = models.EmailField()
    text = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
    post = models.ForeignKey(Article)

    def __str__(self):
        return '{0}: {1}'.format(self.author, self.post.title)


class Evaluate(models.Model):

    class Meta:
        verbose_name = u'评分'
        verbose_name_plural = u'评分'
    ip = models.CharField(max_length=40)
    evaluate = models.IntegerField()
    post = models.ForeignKey(Article)

    def __str__(self):
        return '{0}: {1}'.format(self.ip, self.evaluate)


class Page(models.Model):

    class Meta:
        verbose_name = u'页面'
        verbose_name_plural = u'页面'
    # 作者
    author = models.ForeignKey(User)
    # 标题
    title = models.CharField(max_length=200)
    # 正文
    text = models.TextField()
    # 排列顺序
    porder = models.IntegerField(default=0)
    # 创建时间
    created_date = models.DateTimeField(auto_now_add=True)
    # 发布时间
    publish_date = models.DateTimeField(blank=True, null=True)

    def publish(self):
        self.published_date = datetime.now()
        self.save()

    def __str__(self):
        return self.title


admin.site.register(esptemp, esptempAdmin)
admin.site.register(Author, AuthorAdmin)
admin.site.register(Article, ArticleAdmin)
admin.site.register(Tag)
admin.site.register(Category)
admin.site.register(Comment)
admin.site.register(Evaluate)
admin.site.register(Page)
