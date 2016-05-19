# _*_ coding:UTF-8 _*_
from django.db import models
#from django.utils.html import format_html
#from django.contrib import admin
#from django.contrib.auth.models import User
#import time
import datetime

# Create your models here.

# 装饰器
# 调用函数


def save_log(self, key, **kwargs):
    if self.pk is not None and hasattr(self, key):
        log = {}.fromkeys(['device'], key)
        log.update(author=hasattr(self, 'author') and self.author)
        log.update(room=hasattr(self, 'room') and self.room or None)
        # log.update(light=hasattr(self, 'light') and self.light or None)
        # log.update(light_status=hasattr(self, 'status') and self.status)
        # log.update(hvac=hasattr(self, 'hvac') and self.hvac or None)
        # log.update(hvac_mode=hasattr(self, 'mode') and self.mode or None)
        # log.update(hvac_temperature=hasattr(self, 'temperature')
        #            and self.temperature or None)
        # log.update(curtains=hasattr(self, 'curtains')
        #            and self.curtains or None)
        # log.update(curtains_status=hasattr(self, 'status') and self.status)

        # 这里正常运行，第一次
        if key == 'light':
            log.update(light=self.light)
            log.update(light_status=self.status)
        elif key == 'hvac':
            log.update(hvac=self.hvac)
            log.update(hvac_mode=self.mode)
            log.update(hvac_temperature=self.temperature)
        elif key == 'curtains':
            log.update(curtains=self.curtains)
            log.update(curtains_status=self.status)
        else:
            log = {}
        # 第一次
        # 第二次

        operlog = OperLog(**log)
        operlog.save()

# 装饰器函数


def log_it(key):
    def decorator(func):
        def wrapper(self, *args, **kwargs):
            try:
                save_log(self, key, **kwargs)
            except Exception as e:
                raise e
            finally:
                func(self, *args, **kwargs)
        return wrapper
    return decorator
# 装饰器结束


# def modeltojson(key):
#     def deco(func):
#         def _deco(self):
#             import json
#             fields = func(self)
#             for field in self._meta.fields:
#                 fields.append(field.name)
#             fields.remove('id')
#             d = {}
#             d['pk'] = self.pk
#             for attr in fields:
#                 if isinstance(getattr(self, attr), models.Model):
#                     fmodel = getattr(self, attr)
#                     ffields = []
#                     for ffield in fmodel._meta.fields:
#                         ffields.append(ffield.name)
#                     ffields.remove('id')
#                     fd = {}
#                     fd['pk'] = fmodel.pk
#                     for fattr in ffields:
#                         fd[fattr] = getattr(fmodel, fattr)
#                     d[attr] = fd
#                 elif isinstance(getattr(self, attr), datetime.datetime):
#                     d[attr] = getattr(self, attr).strftime('%Y-%m-%d %H:%M:%S')
#                 else:
#                     d[attr] = getattr(self, attr)
#             if key == 'light':
#                 d['operation_data'] = OperLog.objects.get(
#                     light=self.light).operation_data.strftime('%Y-%m-%d %H:%M:%S')
#             elif key == 'hvac':
#                 d['operation_data'] = OperLog.objects.get(
#                     light=self.light).operation_data.strftime('%Y-%m-%d %H:%M:%S')
#             if isinstance(d, dict):
#                 return json.dumps(d, ensure_ascii=False)
#             else:
#                 return None
#         return _deco
#     return deco

def modeltojson(key):
    def deco(func):
        def _deco(self):
            import json
            fields = func(self)
            data = {}
            if key is not "room":
                for attr in fields:
                    if isinstance(getattr(self, attr), models.Model) and attr is "room":
                        data[attr] = self.room.name
                    elif isinstance(getattr(self, attr), datetime.datetime):
                        data[attr] = getattr(self, attr).strftime(
                            '%Y-%m-%d %H:%M:%S')
                    else:
                        data[attr] = getattr(self, attr)
                oper = OperLog.objects.get(**{key: getattr(self, key)})
                data['operation_data'] = oper.operation_data.strftime(
                    '%Y-%m-%d %H:%M:%S')
                data['operation_user'] = oper.author
                if key in data:
                    # 下面两句等效
                    #data[key +'_position'] = eval("self.get_" + key + "_display()")
                    data[
                        key + '_position'] = getattr(self, 'get_' + key + '_display')()
            else:
                for attr in fields:
                    if isinstance(getattr(self, attr), datetime.datetime):
                        data[attr] = getattr(self, attr).strftime(
                            '%Y-%m-%d %H:%M:%S')
                    else:
                        data[attr] = getattr(self, attr)
            data['pk'] = data.pop(u'id')

            # fields.remove('id')
            # d = {}.fromkeys(['pk'], self.pk)
            # if key in ['light', 'hvac', 'curtains']:
            #     fields.remove('room')
            #     d[key + '_position'] = eval("self.get_" + key + "_display()")
            #     d['room'] = self.room.name
            #     #keywords = {key:getattr(self,key)}
            #     oper = OperLog.objects.get(**{key: getattr(self, key)})
            #     d['operation_data'] = oper.operation_data.strftime('%Y-%m-%d %H:%M:%S')
            #     d['operation_user'] = oper.author
            # for attr in fields:
            #     if isinstance(getattr(self, attr), datetime.datetime):
            #         d[attr] = getattr(self, attr).strftime('%Y-%m-%d %H:%M:%S')
            #     else:
            #         d[attr] = getattr(self, attr)
            # # d.update(dict([(attr, getattr(self, attr))
            # #               for attr in fields]))
            return json.dumps(data, ensure_ascii=False)
        return _deco
    return deco


class Room(models.Model):

    room = models.CharField(u'房间', max_length=8, unique=True)
    name = models.CharField(u'中文名称', max_length=6, unique=True)

    def __unicode__(self):
        return u'%s' % (self.name)

    @modeltojson('room')
    def tojson(self):
        # return [f.name for f in self._meta.fields]
        for f in self._meta.fields:
            yield(f.name)

    class Meta:
        verbose_name = u'房间'
        verbose_name_plural = u'房间'
        ordering = ['id']


# def deco_models_save(func):
#     def _deco(*args, **kwargs):
#         ret, pk = func(*args, **kwargs)
#         if pk is not None:
#             log = {}.fromkeys(['author'], ret.author or None)
#             #log.update(author = ret.author or None)
#             log.update(room=ret.room or None)
#             log.update(device=ret.__class__.__name__.lower() or None)
#             if hasattr(ret, 'light'):
#                 #log.update(device = 'light')
#                 log.update(light=ret.light)
#                 log.update(light_status=ret.status)
#                 #operlog= OperLog(**log)
#                 # operlog.save()
#             elif hasattr(ret, 'hvac'):
#                 log.update(hvac=ret.hvac)
#                 log.update(hvac_mode=ret.mode)
#                 log.update(hvac_temperature=ret.hvac_temperature)
#             elif hasattr(ret, "curtains"):
#                 log.update(curtains=ret.curtains)
#                 log.update(curtains_status=ret.status)
#             operlog = OperLog(**log)
#             operlog.save()
#     return _deco

# 管理器
class LightIsOn(models.Manager):

    def get_queryset(self):
        return super(LightIsOn, self).get_queryset().filter(status=True)

    @property
    def is_on(self):
        return self.filter(status=True)

    @property
    def is_off(self):
        return self.filter(status=False)


class Light(models.Model):
    POSITION_CHOICES = (
        (None, u'名称'),
        (1, u'主灯'),
        (2, u'吸顶灯'),
        (3, u'壁灯'),
        (4, u'灯带'),
        (5, u'台灯'),
        (6, u'落地灯'),
    )
    room = models.ForeignKey(Room, verbose_name=u'房间', blank=True,
                             null=True, related_name='light_room', on_delete=models.SET_NULL)
    light = models.PositiveSmallIntegerField(
        u'电灯位置', default=None, choices=POSITION_CHOICES, help_text=u'1:主灯 2:吸顶灯 3:壁灯 4:灯带 5:台灯 6:落地灯')
    status = models.BooleanField(u'状态', default=False)
    # status_flag = models.CharField(u'状态标志',max_length=8,blank=True,null=True)
    created_date = models.DateTimeField(u'加入时间', auto_now_add=True)

    objects = models.Manager()
    on_of = LightIsOn()

    #@deco_models_save
    @log_it('light')
    def save(self, *args, **kwargs):
        #pk = self.id
        # self.status_flag = self.status and "ON" or "OFF"
        super(Light, self).save(*args, **kwargs)
        # return self, pk
        # save_log
        # if pk is not None:
        #    if hasattr(self, 'author'):
        #        author = self.author
        #    else:
        #        author = u"非法用户"
        #    self.save_log(user=author)

    @modeltojson('light')
    def tojson(self):
        for f in self._meta.fields:
            yield(f.name)
        # return [f.name for f in self._meta.fields]

    def __unicode__(self):
        return "%s::%s::%s" % (self.room, self.light, self.status)

    class Meta:
        verbose_name = u'照明'
        verbose_name_plural = u'照明'
        ordering = ['room', 'light']

    def status_flag(self):
        return self.status and u"开" or u"关"

    status_flag.allow_tags = True
    status_flag.short_description = u"状态"

    def save_log(self, user=None):
        log = {}.fromkeys(['device'], 'light')
        log.update(room=self.room)
        log.update(light_status=self.status)
        log.update(author=user)
        log.update(light=self.light)
        operlog = OperLog(**log)
        operlog.save()


class Hvac(models.Model):
    MODE_CHOICES = (
        (None, u'空调状态'),
        (u'cold', u'制冷'),
        (u'heat', u'制热'),
        (u'auto', u'自动'),
        (u'dry', u'干燥除霉'),
    )
    HVAC_CHOICES = (
        (None, u''),
        (1, u'主空调'),
    )
    room = models.ForeignKey(Room, verbose_name=u'房间', blank=True,
                             null=True, related_name='hvac_room', on_delete=models.SET_NULL)
    hvac = models.PositiveSmallIntegerField(
        u'空调位置', default=None, choices=HVAC_CHOICES, blank=True, null=True)
    mode = models.CharField(u'模式', max_length=4, choices=MODE_CHOICES, default=None,
                            blank=True, null=True, help_text=u'cold:制冷, heat:制热, auto:自动， dry:干燥除霉')
    temperature = models.SmallIntegerField(u'温度', default=0)
    created_date = models.DateTimeField(u'加入时间', auto_now_add=True)

    @log_it('hvac')
    def save(self, *args, **kwargs):
        #pk = self.pk
        super(Hvac, self).save(*args, **kwargs)
        # if pk is not None:
        #    author = hasattr(self, 'author') and self.author or u"非法用户"
        #    self.save_log(user=author)

    @modeltojson('hvac')
    def tojson(self):
        for f in self._meta.fields:
            yield(f.name)

    def __unicode__(self):
        return "%s::%s::%s::%s" % (self.room, self.hvac, self.mode, self.temperature)

    class Meta:
        verbose_name = u'空调'
        verbose_name_plural = u'空调'
        ordering = ['room']

    def save_log(self, user):
        log = {}.fromkeys(['device'], self.__class__.__name__.lower())
        log.update(room=self.room)
        log.update(hvac=self.hvac)
        log.update(hvac_mode=self.mode)
        log.update(hvac_temperature=self.temperature)
        log.update(operation_data=datetime.datetime.now())
        log.update(author=user or None)
        operlog = OperLog(**log)
        operlog.save()
        print str(log)


class Curtains(models.Model):
    room = models.ForeignKey(
        Room, verbose_name=u'房间', blank=True, null=True, on_delete=models.SET_NULL)
    curtains = models.PositiveSmallIntegerField(
        u'窗帘', default=None, blank=True, null=True)
    status = models.BooleanField(u'窗帘状态', default=False)

    @log_it('curtains')
    def save(self, *args, **kwargs):
        #pk = self.pk
        super(Curtains, self).save(*args, **kwargs)
        # if pk is None:
        #    author = hasattr(self, "author") and self.author or u'非法用户'
        #    self.save_log(user=author)

    def save_log(self, user=None):
        log = {}.fromkeys(['device'], 'curtains')
        log.update(room=self.room)
        log.update(curtains=self.curtains)
        log.update(curtains_status=self.status)
        log.update(author=user)
        operlog = OperLog(**log)
        operlog.save()

    class Meta:
        verbose_name = "窗帘"
        verbose_name_plural = "窗帘"

    def __unicode(self):
        return "%s::%s: %s" % (self.room, self.curtains, self.status)


class RoomEnv(models.Model):
    room = models.ForeignKey(Room, verbose_name="房间",
                             blank=True, null=True, on_delete=models.SET_NULL)
    temperature = models.FloatField(u'温度', blank=True, null=True)
    humidity = models.FloatField(u'湿度', blank=True, null=True)
    illumination = models.FloatField(u'照度', blank=True, null=True)
    hvac = models.ManyToManyField(
        Hvac, verbose_name=u'空调', blank=True, null=True)
    light = models.ManyToManyField(
        Light, verbose_name=u'照明', blank=True, null=True)
    onlock = models.BooleanField(u'门锁', default=True)
    curtains = models.ManyToManyField(
        Curtains, verbose_name=u'窗帘', blank=True, null=True)

    class Meta:
        verbose_name = u"家居环境"
        verbose_name_plural = u"家居环境"
        ordering = ['room']

    def __unicode__(self):
        return "%s::temp:%s humi:%s ill:%s" % (self.room, str(self.temperature), str(self.humidity), str(self.illumination))


class OperLog(models.Model):
    LIGHT_CHOICES = (
        (None, u''),
        (1, u'主灯'),
        (2, u'吸顶灯'),
        (3, u'壁灯'),
        (4, u'灯带'),
        (5, u'台灯'),
        (6, u'落地灯'),
    )
    HVAC_CHOICES = (
        (None, u''),
        (1, u'主空调'),
    )

    DEVICE_CHOICES = (
        (None, u'设备'),
        (u'light', u'照明'),
        (u'hvac', u'空调'),
        (u'curtains', u'窗帘'),
    )

    author = models.CharField(u'操作用户', max_length=30,
                              blank=True, null=True)
    operation_data = models.DateTimeField(u'操作时间', auto_now_add=True)
    room = models.ForeignKey(Room, verbose_name=u'房间', blank=True,
                             null=True, related_name='log_as_room', on_delete=models.SET_NULL)
    device = models.CharField(u'操作的设备', choices=DEVICE_CHOICES, max_length=5)
    light = models.PositiveSmallIntegerField(
        u'电灯位置', choices=LIGHT_CHOICES, blank=True, null=True)
    light_status = models.BooleanField(u'照明操作', default=False)
    hvac = models.PositiveSmallIntegerField(
        u'空调位置', choices=HVAC_CHOICES, blank=True, null=True)
    hvac_mode = models.CharField(
        u'空调模式操作', max_length=4, blank=True, null=True)
    hvac_temperature = models.SmallIntegerField(u'操作温度', blank=True, null=True)
    curtains = models.PositiveSmallIntegerField(u'窗帘位置', blank=True, null=True)
    curtains_status = models.BooleanField(u'窗帘操作', default=False)

    def __unicode__(self):
        return "%s::%s::%s" % (self.author, self.operation_data, self.light_status or self.hvac_mode)

    class Meta:
        verbose_name = u'操作记录'
        verbose_name_plural = u'操作记录'
        ordering = ['-operation_data']

    # def display(self):
    #   list_display =['room','author','operation_data','device']
    #   if self.device == "light":
    #       list_display.append('light_status')
    #   if self.device == "hvac":
    #       list_display.append("hvac_mode")
    #       list_display.append("hvac_temperature")
    #   else:
    #       list_display.remove('device')
    #   return list_display
    # display.allow_tags=True

    def display_position(self):
        if self.device == 'light':
            return '%s' % (self.get_light_display())
        elif self.device == 'hvac':
            return "%s" % (self.get_hvac_display())
        else:
            return u"未知"
    display_position.allow_tags = True
    display_position.short_description = "位置"

    MODE_CHOICES = {
        u'cold': u'制冷',
        u'heat': u'制热',
        u'auto': u'自动',
        u'dry': u'干燥除霉',
    }

    def display_device(self):
        if self.device == 'light':
            return '%s' % (u'照明')
        elif self.device == 'hvac':
            return '%s' % ('空调')
        else:
            return u'未知设备'
    display_device.allow_tags = True
    display_device.short_description = u'操作的设备'

    def choices_display(self):
        if self.device == "light":
            return (self.light_status and u"开" or u"关")
        if self.device == "hvac":
            return ('%s' % (self.hvac_mode and (self.MODE_CHOICES.get(self.hvac_mode, "") + "::" + str(self.hvac_temperature) + u"℃") or u'关机'))
        return None
    choices_display.allow_tags = True
    choices_display.short_description = u'操作内容'

    def toJson(self):
        import json
        d = {}
        d['pk'] = self.pk
        d['author'] = self.author
        d['room'] = self.room.name
        d["operation_data"] = self.operation_data.strftime('%Y-%m-%d %H:%M:%S')
        if self.device == 'light':
            d['device'] = u'照明'
            d['light'] = self.get_light_display()
            d['light_status'] = self.light_status and u'开' or u'关'
        elif self.device == 'hvac':
            d['device'] = u'空调'
            d['hvac_mode'] = self.hvac_mode and self.MODE_CHOICES.get(
                self.hvac_mode, None) or u'关机'
            d['hvac_temperature'] = self.hvac_temperature and str(
                self.hvac_temperature) + u'℃' or None
        return json.dumps(d, ensure_ascii=False)
        # return json.dumps(dict([(attr, getattr(self, attr)) for attr in
        # [f.name for f in self._meta.fields]]), ensure_ascii=False)

    def toJsonall(self):
        fields = []
        for field in self._meta.fields:
            fields.append(field.name)
        fields.remove('id')
        d = {}
        for attr in fields:
            # if getattr(self, attr) is None or getattr(self, attr) == "":
            #    pass
            if isinstance(getattr(self, attr), models.Model) and attr == 'room':
                d[attr] = getattr(self, attr).name
            elif isinstance(getattr(self, attr), datetime.datetime):
                d[attr] = getattr(self, attr).strftime('%Y-%m-%d %H:%M:%S')
            elif attr == 'light':
                d['device'] = u'照明'
                d[attr] = self.get_light_display()
            elif attr == 'hvac':
                d['device'] = u'空调'
                d[attr] = self.get_hvac_display()
            # elif attr == 'hvac':
            #    d['device'] = u'空调'
            #    d['hvac'] == self.get_hvac_display()
            elif getattr(self, attr) is True:
                d[attr] = u'开'
            else:
                d[attr] = getattr(self, attr)
        d.update(pk=getattr(self, 'id'))
        import json
        return json.dumps(d, ensure_ascii=False)
# def get_username(req):
#   return req.user.username

# def get_openid(openid):
#   return Weichat.objects.get(openid=openid).nickname


# class Oper(models.Model)

#   author_choices = (
#       (User.objects.get(username=username).username or None,u'网页用户'),
#       (Weichat.objects.get(openid=openid).nickname or None,u'微信用户')，

#       )
#   author = models.CharField(max_length=30,choices = author_choices,default="")

# 获取 models 中的字段名

# models._meta.fields
