# _*_ coding:UTF-8 _*_
from django.db import models
from django.utils import timezone
from datetime import datetime

# Create your models here.


class Device(models.Model):
    name = models.CharField(u'设备名称', max_length=50, unique=True)
    created_date = models.DateTimeField(u'创建时间', auto_now_add=True)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = u'设备表'
        verbose_name_plural = u'设备表'
        ordering = ['name']


class Posts(models.Model):
    device = models.ForeignKey(Device, verbose_name="设备名称")
    temp = models.IntegerField(verbose_name=u"温度", default=0)
    published_date = models.DateTimeField(
        verbose_name=u'上传时间', blank=True, null=True)

    def publish(self):
        self.published_date = datetime.now()
        self.save()

    def __unicode__(self):
        return "%s" % (self.device)

    class Meta:
        verbose_name = u"温度表"
        verbose_name_plural = u'温度表'
        ordering = ['device', '-published_date']


class TestA(models.Model):
    idd = models.AutoField(primary_key=True)
    text = models.CharField(max_length=10)


class TestB(models.Model):
    idb = models.AutoField(primary_key=True)
    idd = models.ForeignKey(TestA, db_column="idd", blank=True, null=True)


class Testfile(models.Model):
    dateform = models.FileField(u'路径', upload_to='./')
    title = models.CharField(u'标题', max_length=50)

    class Meta:
        verbose_name = u"Testfile"
        verbose_name_plural = u"Testfiles"

    def get_absolute_url(self):
        #from django.core.urlresolvers import reverse
        return '/%s/' % self.dateform

    def __unicode__(self):
        return self.title
