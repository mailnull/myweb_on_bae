from django.shortcuts import render_to_response, render, get_object_or_404
from django.http import HttpResponse
from .models import *
from django.db.models.query import QuerySet
from django.core import serializers

# Create your views here.


def display_log(req, pk):
    if pk is not None:
        try:
            logs = OperLog.objects.get(pk=pk)
        except OperLog.DoesNotExist as e:
            logs = {'pk': int(pk), 'status': "error", "msg": e.message}
            # raise e
    else:
        logs = OperLog.objects.all()
    req.session['testsessions'] = "testsessionsTEST"
    a = req.session.get('testsessions', None)
    # try:
    #     del req.session['testsessions']
    # except KeyError:
    #     pass
    if isinstance(logs, QuerySet):
        logs = serializers.serialize('json', logs)
    elif isinstance(logs, dict):
        import json
        logs = json.dumps(logs, ensure_ascii=False)
    else:
        logs = logs.toJson()
    # logs = logs.toJson()
    return HttpResponse(logs, content_type="application/json")
    return render(req, 'display_log.html', {"logs": logs, 'a': a})


# def display_views(request, key):
#     pk = request.GET.get('pk', None)
#     if pk is not None and key is not None:

#     if isinstance(pk, QuerySet):
