# _*_ coding:UTF-8 _*_
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.encoding import smart_str
import time
import hashlib
import os
if 'SERVER_SOFTWARE' in os.environ:
    from lxml import etree as ET
else:
    import xml.etree.ElementTree as ET

from .models import *
from .weichatbase import *


from dwebsocket.decorators import accept_websocket
from django.shortcuts import render


#from .serializers import MessagesSerializer
#from rest_framework import viewsets

#from rendermsg import *
#return_msg = {"text":Textmsg,"image":Imagemsg,"voice":Voicemsg,"video":Videomsg,"shotvideo":ShotVideomsg,"location":Locationmsg,"event":Eventmsg}
# Create your views here.

MY_TOKEN = "weixin"


def websocket_base(request):
    return render(request, 'dwebsocket_base.html', {})

clients = []


@accept_websocket
def websocket_echo(request):
    if request.is_websocket:
        try:
            clients.append(request.websocket)
            for message in request.websocket:
                if not message:
                    break
                for client in clients:
                    client.send(message)
        finally:
            clients.remove(request.websocket)


def index(request):
    # baidu_tts("test")
    df = open("zhishangbugou.mp3", "rb")
    return HttpResponse(df, content_type="audio/mp3")
    return HttpResponse("app weichat index")


@csrf_exempt
def weichatbase(request):
    response = None
    if request.method == "GET":
        response = checksignature(request)
        return HttpResponse(response, content_type="text/plain")
    elif request.method == "POST":
        response = responseMsg(request)
        #response ='<xml><ToUserName><![CDATA[toUser]]></ToUserName><FromUserName><![CDATA[fromUser]]></FromUserName><CreateTime>1348831860</CreateTime><MsgType><![CDATA[text]]></MsgType><Content><![CDATA[你要测试的内容]]></Content><MsgId>1234567890123456</MsgId></xml>'
        return response
    else:
        return HttpResponse(response)


def checksignature(request):

    signature = request.GET.get('signature', None)
    timestamp = request.GET.get('timestamp', None)
    nonce = request.GET.get('nonce', None)
    echostr = request.GET.get('echostr', None)
    token = MY_TOKEN
    tmpList = [token, timestamp, nonce]
    tmpList.sort()
    tmpstr = "%s%s%s" % tuple(tmpList)
    tmpstr = hashlib.sha1(tmpstr).hexdigest()
    if tmpstr == signature:
        return echostr
    else:
        return None
# return
# render_to_response('user_role/api_user.xml',content_type="application/xml")


def responseMsg(request):
    rawstr = smart_str(request.body)
    msg = paraseXML(rawstr)

    # 消息去重
    if check_repeat(msg):
        return HttpResponse(u"success")

    msgtype = msg.get("MsgType", "")
    if msgtype is not None:
        flag = msg_add(msg)
        # if not flag:
        #   return HttpResponse(u"success")
        # msg.pop("CreateTime")
        # msg.update(Content=msg["Content"]+"\n"+str(flag))
        # msg.update(CreateTime=int(time.time()))
        # return render_to_response("reply_text.xml",msg,content_type="application/xml")
        # return HttpResponse(json.dumps(msg,ensure_ascii=False),content_type="application/json")
        # 这里是测试回复语音
        # mm="<xml><ToUserName><![CDATA[%s]]></ToUserName><FromUserName><![CDATA[%s]]></FromUserName><CreateTime>%s</CreateTime><MsgType><![CDATA[voice]]></MsgType><Voice><MediaId><![CDATA[%s]]></MediaId></Voice></xml>"
        #mm=mm %(msg["FromUserName"],msg["ToUserName"],str(int(time.time())),msg["MediaId"])
        # return HttpResponse(mm,content_type="application/xml")
        # 测试语音结束
        # 继续测试
        # msg.pop("Format")
        # msg.pop("Recognition")
        # msg.update(CreateTime=int(time.time()),MediaId="_j2PyrELQMgc494P2RtCluqXK-8RazF0NEadTUvpPkdY9uq72Hg_YrVTX5O_6t-m")
        # return render_to_response("reply_voice.xml",msg,content_type="application/xml")
        # 继续测试结束
        # 测试access_token
        #from weixin_token import WEI_TOKEN
        #mytoken = WEI_TOKEN(msg.get("ToUserName"))
        # return HttpResponse(mytoken.get_and_save_access_token(),content_type="application/json")
        # 测试access_token结束
        # time.sleep(5)
        return replyMsg(msg)
    return HttpResponse(u"success")

# 解析XML


def paraseXML(xml):
    msg = {}
    xml = ET.fromstring(xml)
    if xml.tag == 'xml':
        for child in xml:
            msg[child.tag] = smart_str(child.text)
    return msg

# 数据保存到数据库存


def msg_add(**msg):
    #from copy import deepcopy
    #tempmsg = deepcopy(msg)
    author = msg.pop("ToUserName")
    user = msg.pop("FromUserName")
    try:
        pu = WeiUser.objects.get_or_create(
            openid=user, author=Author.objects.get(author=author))
        pm = Messges(**msg)
        pm.user = pu[0]
        pm.author = pu[0].author
        pm.save()
        #del tempmsg
        return True
    except:
        return False
    return False

def save_msg(func):
    def deco(msg):
        if check_repeat(msg):
            return HttpResponse("success")
        else:
            if msg.get("MsgType",None) is not None:
                msg_add(**msg)



def replyMsg(msg):
    msgtype = msg.pop("MsgType")
    #newmsg,msgtype = handleMsg(msg)
    # return HttpResponse({msgtype:newmsg})
    msgtype, msg = handle_return.get(msgtype)(msg)
    return render_msg.get(msgtype)(msg)
    # return renderMsg(newmsg,msgtype)


def handleMsg(msg):
    msgtype = msg.pop("MsgType")
    msg.update(CreateTime=int(time.time()))
    return msg, msgtype
    return "success"

# # def renderMsg(msg,msgtype):
# #     global return_msg
# #     return return_msg.get(msgtype)(msg)


# # class Handle_and_response():
# #     def __init__(self,**kwargs):
# #         self.msgtype = kwargs.pop("MsgType")
# #         self.msg = kwargs

# #     def textmsg(self):
# #         pass

def handle_textmsg(msg):
    content = msg.pop("Content")
    msg.pop("CreateTime")
    if content in cmdline:
        if checkuser(msg.get("FromUserName", "")):
            return respnse_access_error
        CMD = cmdline.get(content, "")
        return {"Content": homecontrol(CMD)}, "text"
    return {"Content": u"你说的是：" + content}, "text"

# def handle_and_response(msgtype,msg):
#   msg.pop("CreateTime")

#   playload,msgtype = handle_reply.get(msgtype,"")(msg)
#   fromuser = msg.get("FromUserName","")
#   touser = msg.get("ToUserName")
#   msg.update(ToUserName=fromuser,FromUserName=touser,CreateTime=int(time.time()),playload)
#   return msg,msgtype #msg这个一个字典


# #text = {"touser":fromusername,"fromuser":tousername,"CreateTime":int(time.time()),"content":content}
# """
# <xml>
# <ToUserName><![CDATA[toUser]]></ToUserName>
# <FromUserName><![CDATA[fromUser]]></FromUserName>
# <CreateTime>12345678</CreateTime>
# <MsgType><![CDATA[voice]]></MsgType>
# <Voice>
# <MediaId><![CDATA[media_id]]></MediaId>
# </Voice>
# </xml>

# class MsgViewSet(viewsets.ModelViewSet):
#    queryset = Messges.objects.all()
#    serializer_class = MessagesSerializer
