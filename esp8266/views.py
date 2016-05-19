# _*_ coding:UTF-8 _*_
from django.shortcuts import render, render_to_response, get_object_or_404, redirect
from django.http import HttpResponse, Http404
from .models import *
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
import time
# Create your views here.


def index(request):
    posts = Posts.objects.filter(published_date__isnull=False).prefetch_related(
        'device').order_by('device', 'published_date')
    return render_to_response('espindex.html', {'posts': posts})


def list_by_device(request, device):
    # posts = Posts.objects.filter(published_date__isnull=False,device__name=device).prefetch_related('device').order_by('published_date')
    # posts =
    # Device.objects.get(name=device).posts_set.filter(published_date__isnull=False).order_by('published_date')
    posts = Posts.objects.select_related('device__name').filter(
        published_date__isnull=False, device__name=device).order_by('published_date')
    return render_to_response('espindex.html', {'posts': posts, 'device': device})


def list_by_date(request, device, y, m):
    posts = Posts.objects.select_related('device__name').filter(
        published_date__isnull=False, divice__name=device).filter(
        published_date__year=y, published_date__month=m).order_by(
        'published_date')

    return HttpResponse({"posts": posts})


def return_xml(request):
    dic = {"toUser": "aaa", "fromUser": "bbb", "createTime": int(
        time.time()), "content": "this is test render_to_response :xml"}
    return render_to_response("re_xml.xml", dic, content_type="application/xml")
    return HttpResponse({"toUser": "aaa", "fromUser": "bbb", "createTime": int(time.time()), "content": "this is test render_to_response :xml"})

from django import forms
import json


class fileform(forms.ModelForm):

    class Meta:
        model = Testfile
        fields = ['title', 'dateform']
    # TODO: Define form fields here


class Modforms(forms.Form):
    # TODO: Define form fields here

    def __init__(self, *args, **kwargs):
        self.fields = {}
        from copy import deepcopy
        temp_dict = deepcopy(kwargs)
        # kwargs.clear()
        #super(Modforms, self).__init__(*args, **kwargs)
        for k, v in temp_dict.items():
            if isinstance(v, forms.fields.Field):
                self.fields[k] = v
                kwargs.pop(k)

        super(Modforms, self).__init__(*args, **kwargs)


class Login(forms.Form):
    field_in_login = forms.ModelChoiceField(label=u"表单一",
                                            queryset=Device.objects.all(), empty_label="_______")


class Register(forms.Form):
    field_in_register = forms.CharField(label=u"表单二")


@csrf_exempt
def modform(request):
    if request.method == "POST":
        if "field_in_login" in request.POST:
            form = Login(request.POST)
            if form.is_valid():
                return HttpResponse(form.cleaned_data["field_in_login"])
        elif "field_in_register" in request.POST:
            form = Register(request.POST)
            if form.is_valid():
                return HttpResponse(form.cleaned_data["field_in_register"])
    login = Login()
    register = Register()
    return render(request, "modform.html", {"login": login, "register": register})

    # f = MM(initial={"mod": "esp01"})
    # if request.method == "POST":
    #     f = MM(request.POST)
    #     return HttpResponse(f.mod)

    #     if f.is_valid():
    #         return HttpResponse(f.cleaned_data['mod'])
    # return render(request, "modform.html", {"form": f})
    # qu = Device.objects.all()
    # # ins = qu.get(pk=1)
    # f = Modforms(mod=forms.ModelChoiceField(queryset=qu))
    # # f.fields.update(mod=forms.ModelChoiceField(queryset=qu, initial=ins))
    # if request.method == "POST":
    #     # f.fields.mod = qu.get(pk=request.POST.get("mod"))
    #     f = Modforms(request.POST)
    # #     f.fields.mod = qu.get(pk=f.mod)
    # #     # return HttpResponse(d)
    #     if f.is_valid():
    #         #         f = f.initial = qu.get(pk=2)
    #         return HttpResponse("success")
    # #     else:
    # #         return HttpResponse("error")
    # return render(request, "modform.html", {"form": f})
    # # pass


@csrf_exempt
def fileupdate(request):
    if request.method == "POST":
        form = fileform(request.POST, request.FILES)
        # return HttpResponse(request.FILES['dateform'])
        if form.is_valid():

            p = form.save(commit=True)
            return render_to_response('fileupdate.html', {"forms": form})
    else:
        form = fileform()
    return render_to_response('fileupdate.html', {'forms': form})


@csrf_exempt
def jsontest(request):
    if request.method == "POST":
        data = json.loads(request.body)
        for i in data:
            print "%s = %s" % (i, data[i])
        data.update(name=66, sex=44)
        # return HttpResponse(data, content_type="application/json")
        return HttpResponse(json.dumps(data), content_type="application/json")
        # content_type="application/json")
    return render_to_response("jsontest.html", {})


def getweb(num):
    import requests
    import time
    url = "http://hbcw.xyz:8081"
    while num:

        try:
            r = requests.get(url)
            if r.ok:
                print r.headers["Date"]
                time.sleep(1)
                r.close()
        except:
            print "error"
        num -= 1


def testthread(num, lst, func):
    import thread
    while num:
        thread.start_new_thread(func, (lst,))
        print "start new :%s" % (num)
        num -= 1
