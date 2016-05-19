# _*_ coding:UTF-8 _*_
from django.contrib import admin
from .models import *
from django.db import models
from django import forms
# Register your models here.


class LightInline(admin.TabularInline):
    model = Light


class HvacInline(admin.TabularInline):
    model = Hvac


class CurtainsInline(admin.TabularInline):
    model = Curtains


class RoomAdmin(admin.ModelAdmin):
    list_display = ['room', 'name']
    inlines = [LightInline, HvacInline, CurtainsInline]

    def get_readonly_fields(self, request, obj=None):

        if request.user.is_superuser:
            pass
        else:
            readonly_fields = [x.name for x in obj._meta.fields]
            readonly_fields.pop(0)
            self.readonly_fields = readonly_fields
        return super(RoomAdmin, self).get_readonly_fields(request, obj)


class LightAdmin(admin.ModelAdmin):
    list_display = ['room', 'light', 'status', 'status_flag', 'created_date']
    list_display_links = ["room", "status"]
    # readonly_fields = ['status_flag']
    # fields = ('room', ('light', 'status'))
    # radio_fields = {"room":admin.HORIZONTAL,"light":admin.HORIZONTAL}
    # #HORIZONTAL or VERTICAL
    fieldsets = (
        (u'照明状态', {
            'fields': ('status',)
        }),
        (u'房间和照明位置', {
            "classes": ('wide', 'extrapretty'), "fields": ('room', 'light',)
        }),
    )

    def save_model(self, request, obj, form, change):
        obj.author = request.user.get_username() or None 
        super(LightAdmin, self).save_model(request, obj, form, change)

    def get_readonly_fields(self, request, obj=None):

        if request.user.is_superuser:
            pass
        else:
            #   readonly_fields = [ x.name for x in obj._meta.fields]
            #   readonly_fields.pop(0)
            self.readonly_fields = ['room']
        return super(LightAdmin, self).get_readonly_fields(request, obj)


class HvacAdmin(admin.ModelAdmin):
    list_display = ['room', 'hvac', 'mode', 'temperature', 'created_date']

    def save_model(self, request, obj, form, change):
        obj.author = request.user.get_username() or "None"
        obj.save()

    def get_readonly_fields(self, request, obj=None):

        if request.user.is_superuser:
            pass
        else:
            #       readonly_fields = [ x.name for x in obj._meta.fields]
            #       readonly_fields.pop(0)
            self.readonly_fields = ['room']
        return super(HvacAdmin, self).get_readonly_fields(request, obj)


class RoomEnvAdmin(admin.ModelAdmin):

    filter_horizontal = ['hvac']
    # filter_vertical = ['light']


class OperLogAdmin(admin.ModelAdmin):

    list_display = ['room', 'author', 'display_device',
                    'display_position', 'choices_display', 'operation_data']
    list_display_links = ['room', 'display_device']
    # list_filter = ['light_status', 'hvac_mode', 'curtains_status']
    search_fields = ['author']
    empty_value_display = 'unknown'
    #

    def get_readonly_fields(self, request, obj=None):

        if request.user.is_superuser:
            pass
        else:
            readonly_fields = [x.name for x in obj._meta.fields]
            device = obj.device
            if device == "light":
                readonly_fields.pop(readonly_fields.index('light'))
                readonly_fields.pop(readonly_fields.index('light_status'))

            elif device == 'hvac':
                readonly_fields.pop(readonly_fields.index('hvac'))
                readonly_fields.pop(readonly_fields.index('hvac_mode'))
                readonly_fields.pop(readonly_fields.index('hvac_temperature'))

            readonly_fields.pop(0)
            self.readonly_fields = readonly_fields
        return super(OperLogAdmin, self).get_readonly_fields(request, obj)

    def get_form(self, request, obj=None, **kwargs):
        self.exclude=[]
        if obj is None:
            pass #return super(OperLogAdmin, self).get_form(request, obj, **kwargs)
        else:
            if obj.device == 'light':
                self.exclude = ["hvac_mode", "hvac_temperature",
                            'hvac', 'curtains', 'curtains_status']

            elif obj.device == 'hvac':
                self.exclude = ['light', 'light_status',
                            'curtains', 'curtains_status']
            elif obj.device == 'curtains':
                self.exclude = ['light', 'light_status',
                            'hvac_mode', 'hvac_temperature', 'hvac']
            else:
                pass#return super(OperLogAdmin, self).get_form(request, obj, **kwargs)
        return super(OperLogAdmin, self).get_form(request, obj, **kwargs)
    #     super(OperLogAdmin, self).get
    # list_display=['display']

    # def get_list_display(self,request):
    #   plight = OperLog.objects.filter(device = "light")
    #   if plight:
    #       self.list_display =['room','light_status']
    # obj1 = OperLog.objects.filter(device="hvac")
    # if obj1:
    # self.list_display=['room','hvac_mode','hvac_temperature']

    #   return super(OperLogAdmin,self).get_list_display(request)
admin.site.register(Room, RoomAdmin)
admin.site.register(Light, LightAdmin)
admin.site.register(Hvac, HvacAdmin)
admin.site.register(OperLog, OperLogAdmin)
admin.site.register(Curtains)
admin.site.register(RoomEnv, RoomEnvAdmin)
