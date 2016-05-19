# -*- encoding: utf-8 -*-
"""
Topic: 全局处理器
Desc : 
"""
from .. import models
from . import utils
from django.db import connection
from django.db.models import Count
from datetime import timedelta
from django.utils import timezone

# 使用context processro去提供一些context内容中公共的部分，也就是返回一个字典而已。
def custom_proc(request):
    # 显示前5个页面，安装porder排序
    recent_pages = models.Page.objects.filter(
        publish_date__isnull=False).order_by('porder')[:5]
    # 近期文章
    recent_posts = models.Article.objects.filter(
        publish_date__isnull=False).order_by('-published_date')[:10]
    # 热门文章
    old_month = timezone.now() - timedelta(days=60)
    hot_posts = models.Article.objects.annotate(num_comment=Count('comment')).filter(
        publish_date__gte=old_month).prefetch_related(
        'category').prefetch_related('tags').order_by('-click')[:10]
    # 近期评论
    recent_comments = models.Comment.objects.prefetch_related(
        'post').order_by('-created_date')[:10]
    # 标签
    alltags = models.Tag.objects.annotate(num_post=Count('name'))
    tags = {t.name: t.num_post for t in alltags}
    # 分类目录
    categories = models.Category.objects.annotate(
        num_post=Count('name')).filter(num_post__gt=0).order_by('name')
    # 文章归档，按照年月分类
    select = {
        'year': connection.ops.date_trunc_sql('year', 'publish_date'),
        'month': connection.ops.date_trunc_sql('month', 'publish_date'),
    }
    archives = models.Article.objects.filter(publish_date__isnull=False).extra(
        select=select).values('year', 'month').annotate(number=Count('id'))
    for ar in archives:
        ar['year'] = ar['year'].year
        ar['month'] = ar['month'].month
    return {
        'RECENT_PAGES': recent_pages,
        'RECENT_POSTS': recent_posts,
        'HOT_POSTS': hot_posts,
        'RECENT_COMMENTS': recent_comments,
        'TAGS': utils.tag_font(tags),
        'CATEGORIES': categories,
        'ARCHIVES': archives,
    }