'''
硬件相关:
	供应商，制造商，出厂日期，服务器类型，st/sn, 自定义资产号，idc, 机柜，机柜内位置，到保日期，有无ups，
	上架日期，raid, raid卡型号，远程管理卡类型，远程管理卡ip, 电源功率，是否是虚拟机，宿主机
系统相关
	操作系统类型，操作系统版本，主机名，内网Ip，mac地址，cpu型号，硬盘信息，内存信息，服务器状态，备注
业务相关
	业务线，产品线，故障处理人，运维接口人，开发人
	
API需求分析
	请求：
		版本号: "2.0"
		方法: "host.get"
		ID: 1
		认证: None
		参数: {
				输出字段: []
				查询个数: 
				排序
				}
	应答：
		版本号： "2.0"
		结果: []
		ID： 1
		
'''
#API.py
	class AutoLoad(object):
		'''
		自动加载类
		'''
		def isValidMethod(self, func=None):
			'''
			判断方法是否可用
			'''
		def isValidModule(self):
			'''
			判断模块是否可用
			'''
		def getCallMethod(self):
			'''
			返回可执行方法
			'''
		def _load_module(self):
			'''
			加载模块
			'''
			
class Response(object):
	'''
	自定义一个返回对象
	'''
	def __init__(self,data):
		self.data = data    #返回的数据
		self.errorCode = 0  #错误码
		self.errorMessage = None  #错误信息
class JsonRpc(object):
	def execute(self):
		'''
		执行指定的方法
		返回执行后的结果
		'''
	def callMethod(self, module, func, params, auth):
		'''
		加载模块，验证模块是否可加载，函数是否可调用
		验证权限
		执行方法
		返回结果
		module：记住转换成小写字母
		'''

	def requireAuthentication(self, module, func):
		'''
		判断需要执行的API是否需要验证
		'''
	def validate(self):
		'''
		验证json, 以及json传参
		'''
	def jsonError(self, id, errno, data=None):
		'''
		处理json
		'''
	def processResult(self, response):
		'''
		处理执行后的返回结果
		'''
	def isError(self):
		'''
		返回是否有错
		'''