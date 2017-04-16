import hashlib
import xml.etree.ElementTree as ET
from tornado import web

class Auth(web.RequestHandler):
	def get(self):
		echostr   = request.method.get['echostr']  #单独验证此值或验证下面三个值
		signature = request.method.get['signature']  
		timestamp = request.method.get['timestamp']
		token     = request.method.get['token']
		nonce     = request.method.get['nonce']
		authstr   = ''.join(sorted([timestamp, token, nonce]))
		auth_hex_sha1 = hashlib.sha1(authstr).hexdigest()
		if auth_hex_sha1 == signature:
			return echostr
		else:
			return False
			
	def post(self):
		data = self.request.body  #self.get_body_argument()
		root = ET.parse(data)
		toUser = root.findtext(".//ToUserName")
		fromUser = root.findtext(".//fromUser")
		CreateTime = root.findtext(".//CreateTime")
		repl = '''
		<xml>
		   <ToUserName><![CDATA[{fromUser}]]></ToUserName>
		   <FromUserName><![CDATA[{toUser}]]></FromUserName> 
		   <CreateTime>{CreateTime}</CreateTime>
		   <MsgType><![CDATA[text]]></MsgType>
		   <Content><![CDATA[this is a test]]></Content>
		   <MsgId>1234567890123456</MsgId>
		   <AgentID>1</AgentID>
		</xml>
		'''.format({
			'toUser':toUser,
			'fromUser': fromUser,
			'CreateTime': 'CreateTime'
		})
		return repl
		