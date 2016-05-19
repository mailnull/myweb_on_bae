# -*- coding: utf-8 -*-
import time
import urllib2
import json
import urllib

from .models import Access_token, Author, Baidu_author, Baidu_access_token


class WEI_TOKEN():

    def __init__(self, touser):
        __app_ID = {"gh_faabb9a450dd": {"appid": "wxa5c5c6a48aeb3a89", "appsecret": "297fbd89137f9f187c726b8da6f42dda"},
                    "gh_b46e07012e44": {"appid": "wxc5226338262dee39", "appsecret": "dba19fc1373b99215753a18185dc22ee"}}
        __url = "https://api.weixin.qq.com/cgi-bin/token"
        __params = {"grant_type": "client_credential",
                    "appid": __app_ID[touser]["appid"],
                    "secret": __app_ID[touser]["appsecret"]
                    }
        __url_valurs = urllib.urlencode(__params)
        self._full_url = __url + "?" + __url_valurs
        self.openid = touser

    def __get_access_token(self):
        _res = urllib2.urlopen(self._full_url)
        if int(_res.code) == 200:
            response_json = json.loads(_res.read())
        else:
            response_json = None
        return response_json

    def get_and_save_access_token(self):
        now = int(time.time())
        # ,expires_in__gte=now-7200+60)
        p = Access_token.objects.filter(author__author=self.openid)
        if p:
            if p[0].expires_in >= (int(time.time()) - 7200 + 60):
                return p[0].access_token
            else:
                jsondate = self.__get_access_token()
                if jsondate != None:
                    p[0].access_token = jsondate["access_token"]
                    p[0].expires_in = int(time.time())
                    p[0].save()
                    return p[0].access_token

        else:
            jsondate = self.__get_access_token()
            if jsondate != None:

                jsondate.update(expires_in=int(time.time()))
                # return json.dumps(jsondate)
                p = Access_token(**jsondate)
                p.author = Author.objects.get(author=self.openid)
                p.save()

                return p.access_token


class BAIDU_token():

    def __init__(self, App_ID):
        __p = None
        self.exist_App_ID = False
        try:
            __p = Baidu_author.objects.get(App_ID=App_ID)
        except:
            pass
        if __p:
            self.author = __p
            self.exist_App_ID = True
            self.App_ID = App_ID
            self.API_Key = __p.API_Key
            self.Secret_Key = __p.Secret_Key
            self.url = 'https://openapi.baidu.com/oauth/2.0/token'
            self.data = {'grant_type': 'client_credentials',
                         'client_id': self.API_Key, 'client_secret': self.Secret_Key}

    def __get(self):
        if self.exist_App_ID:
            request = urllib2.Request(
                url=self.url, data=urllib.urlencode(self.data))
            res = urllib2.urlopen(request)
            if int(res.code) == 200:
                return json.loads(res.read())
            else:
                return {}
        else:
            return {}

    def get_and_save(self):
        now = time.time()
        try:
            p = Baidu_access_token.objects.get(App_ID=self.App_ID)
        except:
            p = None
        if p:
            if p.expires_in >= (int(now) - 86400 + 60):
                return p.access_token
            else:
                jsondate = self.__get()
                if jsondate is not None:
                    p.access_token = jsondate['access_token']
                    p.expires_in = now
                    p.save()
                    return p.access_token
        else:
            jsondate = self.__get()
            if jsondate is not None:
                p = Baidu_access_token()
                p.access_token = jsondate.pop('access_token')
                p.author = self.author
                p.App_ID = self.App_ID
                p.expires_in = now
                p.save()
                return p.access_token
        return None
