# _*_ coding:UTF-8 _*_
from django.shortcuts import render_to_response
import urllib2
import time
from io import BytesIO
from StringIO import StringIO
import requests
from xiaoichat import ichat
from weixin_token import *
from .models import *

xiaoiNoanswer = [u"主人还没有给我设置这类话题的回复，你帮我悄悄的告诉他吧！",
                 u"主人还没给我设置这类话题的回复，你帮我悄悄的告诉他吧~"]


def Textmsg(msg):
    return render_to_response("reply_text.xml", msg, content_type="application/xml")


def Voicemsg(msg):
    return render_to_response("reply_voice.xml", msg, content_type="application/xml")

render_msg = {"text": Textmsg, "voice": Voicemsg}
#return_msg = {"text":Textmsg,"image":Imagemsg,"voice":Voicemsg,"video":Videomsg,"shotvideo":ShotVideomsg,"location":Locationmsg,"event":Eventmsg}


def handle_text(msg):
    Content = msg.pop("Content")
    reply_MsgType = "text"
    chat_xiaoi = ichat(msg["FromUserName"][:5])
    chat_answer = chat_xiaoi.ask_answer(Content)
    if chat_answer in xiaoiNoanswer:
        chat_answer = u"机器人智商不够了"

    msg.update(Content=chat_answer, CreateTime=int(time.time()))
    return reply_MsgType, msg


def handle_voice(msg):
    # msg.update(CreateTime=int(time.time()),MediaId="JuD3SKSudWZxJoLbFt8iKYaeYtXO7-FczDeSUHed8wfcxengCHnKFDASO9N5wKsj")
    #replay_MsgType = "voice"
    # return replay_MsgType,msg

    recognition = msg.pop("Recognition")
    reply_MsgType = "text"
    chat_xiaoi = ichat(msg["FromUserName"][:5])
    chat_answer = chat_xiaoi.ask_answer(recognition)
    # if chat_answer in xiaoiNoanswer:
    #   msg.update(CreateTime=int(time.time()),MediaId="A0VuPzuinL5w3qnvTz0p-GmcaRH8ZwolOu7OcSKMDzFw-sGUCM5zrFWKc8SljfAw")
    #   reply_MsgType="voice"
    #   return reply_MsgType,msg
    # 调试开始
    author = msg["ToUserName"]
    if check_type(author):
        #jsondata = upload_temp_file()
        #jsondata = baidu_tts(chat_answer, author)
        jsondata = test2audio(chat_answer, author)
        msg.update(CreateTime=int(time.time()), MediaId=jsondata["media_id"])
        reply_MsgType = "voice"
    else:
        msg.update(CreateTime=int(time.time()), Content=chat_answer)
    return reply_MsgType, msg

    #   return reply_MsgType,msg
    # 调试结束
    newmsg = u"我说的是：%s\n机器人的回答：%s\n%s" % (
        recognition, chat_answer, msg["MediaId"])
    msg.update(Content=newmsg, CreateTime=int(time.time()))
    return reply_MsgType, msg


def handle_image(msg):
    msg.update(CreateTime=int(time.time()), Content=u"图片我还不会看！")
    return 'text', msg


def handle_video(msg):
    msg.update(CreateTime=int(time.time()), Content=u"视频我还不会看!")
    return 'text', msg


def handle_shortvideo(msg):
    msg.update(CreateTime=int(time.time()), Content=u"视频我还不会看!")
    return 'text', msg


def handle_location(msg):
    msg.update(CreateTime=int(time.time()), Content=u"地图我还不会看!")
    return 'text', msg


def handle_link(msg):
    msg.update(CreateTime=int(time.time()), Content=u"链接网页我也打不开，你自己先看看吧!")
    return 'text', msg


def handle_event(msg):
    msg.update(CreateTime=int(time.time()), Content=u"事件消息我也不会读！")
    return 'text', msg

handle_return = {"text": handle_text, "voice": handle_voice, "image": handle_image, "video": handle_video,
                 "shortvideo": handle_shortvideo, "location": handle_location, "link": handle_link, "event": handle_event}


# yuyin_API_get_token="https://openapi.baidu.com/oauth/2.0/token%EF%BC%9Fgrant_type=client_credentials&client_id=moCAj9lb2Vyc1AS1XRmcYlgx&client_secret=d4076ac92eb4a1ac624c9240a86ec98b&"
# apiJSON={
#     "access_token": "24.fcd98ed84a60edac5570bad358f0a51c.2592000.1462249742.282335-7954404",
#     "session_key": "9mzdXRcGKp40C1RbRA/b/9TI+lt6Nk8gOVGMOrXqrhDLtc/M91JaC1C8TVgdZkIo2XI8USK3EedJDuBGJFM8NDKs9xUn",
#     "scope": "public audio_tts_post wise_adapt lebo_resource_base lightservice_public hetu_basic lightcms_map_poi kaidian_kaidian",
#     "refresh_token": "25.7d41488851dc1b42abd91ee8606fe9e3.315360000.1775017742.282335-7954404",
#     "session_secret": "41a8fa89813e1c171f232beb64b2d3e5",
#     "expires_in": 2592000
# }

# {
#     "access_token": "YI4Wb-uRGv0QPf15zCTHcYnHD-weN7DSPonzh26UUI2bu1pamx3bn9LeWrg15J07_0CjeXg7TSAZx25M90nMGL7lgjIX6r-thr2VVyI5J80n1jf_cldn49NBdNIPlP3hAGBiACADJE",
#     "expires_in": 7200
# }

def upload_temp_file():
    access_token = "qd0KYjDw6YO_I58RkrdPqgZtBeuk5_nAGrvYjWQAkxXTKr_maZC40itPjapWT7l3r28qrixjgbYDJNHTx_espzO9IJZuTwGcwMFN4ULBX7bw3_QuwGW8bwkX5pQkGQUEARZgABAWNV"
    url = "https://api.weixin.qq.com/cgi-bin/media/upload?access_token=%s&type=voice" % (
        access_token)
    from poster.encode import multipart_encode
    from poster.streaminghttp import register_openers
    register_openers()
    datagen, headers = multipart_encode(
        {"filename": open("zhishangbugou.mp3", "rb")})
    request = urllib2.Request(url, datagen, headers)
    result = urllib2.urlopen(request)
    # return result.read()
    if result.code == 200:
        date = json.loads(result.read())
        return date
    return None


def baidu_tts(text, touser):
    url = "http://tsn.baidu.com/text2audio?tex=%s&lan=zh&ctp=1&cuid=c18013792913&tok=%sspb=6"
    token = "24.fe6aa4ee58e8253f893f4434dfa417d7.2592000.1462250664.282335-7954404"
    urltest = "http://tsn.baidu.com/text2audio?tex=%s&lan=zh&ctp=1&cuid=c18013792913&tok=24.fe6aa4ee58e8253f893f4434dfa417d7.2592000.1462250664.282335-7954404"
    # req=url%(text,token)
    text = text.encode('utf8')
    text = urllib.quote(text)
    url = url % (text, token)
    res = urllib2.urlopen(url)
    # if res.code ==200:
    f = open("zhishangbugou.mp3", "wb")
    f.write(res.read())
    f.close()
    #import StringIO
    #fp = StringIO.StringIO(res.read())
    new_access_token = WEI_TOKEN(touser)
    access_token = new_access_token.get_and_save_access_token()

    # access_token="n9tquWmIQV7HUPr5MNKO90w3V-m6k6oLKJFExQUTyqJ3o-xOMkeafd3tqxAP-NmgsxRj5vIRtxyrCDGSwu5d5Lpuq2cOrPdmmLF-cG61sRnFveGCkRvJTwB65hpsJSTsGPAeACAXGR"
    url = "https://api.weixin.qq.com/cgi-bin/media/upload?access_token=%s&type=voice" % (
        access_token)
    from poster.encode import multipart_encode
    from poster.streaminghttp import register_openers
    register_openers()
    #datagen, headers = multipart_encode({"filename":fp})
    datagen, headers = multipart_encode(
        {"filename": open("zhishangbugou.mp3", "rb")})
    request = urllib2.Request(url, datagen, headers)
    import json
    result = urllib2.urlopen(request)
    return json.loads(result.read())
    return True
    return False


def test2audio(text, touser):
    tts_url = "http://tsn.baidu.com/text2audio?tex=%s&lan=zh&ctp=1&cuid=c18013792913&tok=%sspb=6"
    baidu = BAIDU_token(7954404)
    baidu_access_token = baidu.get_and_save()
    if baidu_access_token:
        text = urllib.quote(text.encode('utf8'))
        res = urllib2.urlopen(tts_url % (text, baidu_access_token))
        fp = StringIO(res.read())
        #fp = BytesIO(res.read())

    else:
        fp = None
    if fp:
        new_access_token = WEI_TOKEN(touser)
        access_token = new_access_token.get_and_save_access_token()
        url = "https://api.weixin.qq.com/cgi-bin/media/upload?access_token=%s&type=voice" % (
            access_token)
        files = {'filename': ('baidutts.mp3', fp)}
        r = requests.post(url, files=files)
        return r.json()


def check_repeat(msg):
    if 'MsgId' in msg:
        lastmsg = Messges.objects.filter(
            user__openid=msg['FromUserName'], MsgId=msg['MsgId'])
    else:
        lastmsg = Messges.objects.filter(
            user__openid=msg['FromUserName'], CreateTime=msg['CreateTime'])
    # last={}
    if lastmsg:
        #last.update(CreateTime = lastmsg.CreateTime,newmsg = msg["CreateTime"])
        # return last
        # if int(msg['CreateTime']) == int(lastmsg.CreateTime):
        return True
    return False


def check_type(author):
    author_type = Author.objects.get(author=author)
    '''
    authorType = (
        (None,u"账号类型"),
        (0, u"订阅号"),
        (1, u"服务号"),
        (2, u"认证订阅号"),
        (3, u"认证服务号"),
        (4, u"测试号"),
        )
    '''
    if author_type.author_type > 2:
        return True
    return False


def author_type_checked(msgtype):
    def deco(func):
        def wrapper(msg):
            author_type = Auhtor.objects.get(author=msg['ToUserName'])
            if author_type > 2:
                return func(msg)
            else:
                return response_textmsg(msg)
        return wrapper
    return deco


def response_textmsg(msg):
    return None
