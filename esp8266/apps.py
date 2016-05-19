# _*_ coding:UTF-8 _*_
from django.apps import AppConfig
from .models import Device
import datetime


class Esp8266AppConfig(AppConfig):
    name = 'esp8266'
    verbose_name = u'espwifi'

    def ready(self):
        l = Device.objects.get(pk=1)
        print "%s,%s" % (l.name, datetime.datetime.now())
        print '-------------start app esp8266----------------'
