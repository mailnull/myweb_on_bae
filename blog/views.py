# _*_ coding:UTF-8 _*_
from django.shortcuts import render, render_to_response, get_object_or_404, redirect
from django.http import HttpResponse, Http404
from django.core.urlresolvers import reverse
from django.views.decorators.csrf import csrf_exempt
from django.template import RequestContext
from .models import esptemp, Author, Article, Comment, Tag, Category, Evaluate, Page
import json
from datetime import datetime, timedelta
from django.http import HttpResponse
from .forms import PostForm, CommentForm
from django.contrib.auth.decorators import login_required
from django.db import connection
from django.db.models import Count
from django.contrib.auth.models import User

# Create your views here.


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

# def getnickname(request):
#   nickname = {}
#   if request.user.is_authenticated():
#       pnick=User.objects.select_related().get(username=request.user)
#       nickname={"nickname":pnick.author.nickname if True else ""}
#   return nickname


def index(request):
        #posts = Article.objects.filter(publish_date__isnull=False).order_by('-publish_date')
    posts = Article.objects.annotate(num_comment=Count('comment')).filter(
        publish_date__isnull=False).prefetch_related(
        'category').prefetch_related('tags').prefetch_related('author').order_by('-publish_date')
    # for p in posts:
    #   p.click = cache_manager.get_click(p)
    return render_to_response('blog_list.html', {"posts": posts}, context_instance=RequestContext(request))
    return HttpResponse(" app blog index")


def post_list_by_tag(request, tag):
    """根据标签列出已发布文章"""
    posts = Article.objects.annotate(num_comment=Count('comment')).filter(
        publish_date__isnull=False, tags__name=tag).prefetch_related(
        'category').prefetch_related('tags').order_by('-publish_date')
    for p in posts:
        p.click = cache_manager.get_click(p)
    return render(request, 'post_list.html',
                  {'posts': posts, 'list_header': '文章标签 \'{}\''.format(tag)})


def post_list_by_category(request, cg):
    """根据目录列表已发布文章"""
    posts = Article.objects.annotate(num_comment=Count('comment')).filter(
        publish_date__isnull=False, category__name=cg).prefetch_related(
        'category').prefetch_related('tags').order_by('-publish_date')
    for p in posts:
        p.click = cache_manager.get_click(p)
    return render_to_response('post_list.html', {'posts': posts, 'list_header': '\'{}\' 分类的存档'.format(cg)}, context_instance=RequestContext(request))


def post_detail(request, pk):
    post = get_object_or_404(Article, pk=pk)
    return render_to_response("post_detail.html", {"post": post}, context_instance=RequestContext(request))


@login_required
@csrf_exempt
def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            # post.author=request.user
            post.author = Author.objects.get(user=request.user)
            ptags = request.POST['tags'].strip()
            all_tags = []
            if ptags:
                tags = ptags.split(',')
                for tag in tags:
                    try:
                        t = Tag.objects.get(name=tag)
                    except Tag.DoesNotExist:
                        t = Tag(name=tag)
                        t.save()
                    all_tags.append(t)
            post.save()
            for tg in all_tags:
                post.tags.add(tg)

            return redirect('blog.views.post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render_to_response('post_edit.html', {'form': form, "is_new": True}, context_instance=RequestContext(request))


@login_required
@csrf_exempt
def post_edit(request, pk):
    post = get_object_or_404(Article, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = Author.objects.get(user=request.user)
            # post.update_pubdata()
            post.save()
            return redirect('blog.views.post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render_to_response('post_edit.html', {'form': form}, context_instance=RequestContext(request))


def post_draft_list(request):
    posts = Article.objects.filter(
        publish_date__isnull=True).order_by('-created_date')
    return render_to_response('post_draft_list.html', {'posts': posts}, context_instance=RequestContext(request))


def post_publish(request, pk):
    post = get_object_or_404(Article, pk=pk)
    post.publish()
    return redirect('blog.views.post_detail', pk=pk)


def post_remove(request, pk):
    post = get_object_or_404(Article, pk=pk)
    post.delete()
    return redirect('blog.views.index')


def testblog(request):
    import json
    dic = json.dumps({"json": "正常"}, ensure_ascii=False)
    return HttpResponse(dic)


@csrf_exempt
def temp(request):
    dic = ""
    if request.method == "POST":
        device = request.POST.get("device", '')
        temp = request.POST.get("temp", '')
        p = esptemp.objects.get_or_create(device=device, temp=temp)
        if p[1]:
            dic = json.dumps({"status": "add new device success!", "device": p[
                             0].device, "temp": p[0].temp})

        else:
            p[0].temp = temp
            p[0].save()
            dic = json.dumps({"status": "updata temp success!",
                              "device": p[0].device, "temp": p[0].temp})

        return HttpResponse(dic, content_type="application/json")
    device = request.GET.get("device", "")
    if device:
        p = esptemp.objects.filter(device=device)
        if p.exists():
            temp = p[0].temp
            dic = json.dumps({"status": "get temp success!",
                              "device": device, "temp": temp})
        else:
            dic = json.dumps(
                {"status": "fail", "msg": "device is not exists!"})
        return HttpResponse(dic)
    pall = esptemp.objects.all()
    dic = {}
    for i in pall:
        dic[i.device] = i.temp
    dic = json.dumps(dic)
    return HttpResponse(dic)


def testjson(req):
    return render_to_response("testjson.html", {"jsondate": json.dumps({"key": u"值"}, ensure_ascii=False)})
