# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )

import xiaoi.ibotcloud
api_key="rJP10FDcmf2x"
api_sec = "xjoiTxmzdZnS1bs7tnIT"

class ichat():
	def __init__(self,userid):
		self._api_key=api_key
		self._api_sec=api_sec
		self._userid=userid
		__signature_ask=xiaoi.ibotcloud.IBotSignature(app_key=self._api_key,
                                              app_sec=self._api_sec,
                                              uri="/ask.do",
                                              http_method="POST")
		__params_ask = xiaoi.ibotcloud.AskParams(platform="custom",
                                       user_id=self._userid,
                                       url="http://nlp.xiaoi.com/ask.do")
		self.ask_session=xiaoi.ibotcloud.AskSession(__signature_ask, __params_ask)

	def ask_answer(self,question):
		
		ret_ask = self.ask_session.get_answer(question)
		if ret_ask.http_status!=200:
			ret_ask="服务器正在升级中......."
		return ret_ask.http_body



