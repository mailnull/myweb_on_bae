# _*_ coding:UTF-8 _*_
from django.apps import AppConfig


class MyhomeAppConfig(AppConfig):
    name = 'myhome'
    verbose_name = u'家居'

    def ready(self):
        print '-------------start app myhome ----------------'
