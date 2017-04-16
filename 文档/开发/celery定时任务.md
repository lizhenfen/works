固定配置文件:
	app.conf.broker_url='redis://:passwd@localhost:8667/0'  #指定broker; redis+socket  使用socket; 默认使用amqp
	app.conf.broker_transport_options = {'visibility_timeout': 3600}  # 1 hour.任务超时前的等待时间
	app.conf.result_backend = 'redis://localhost:6379/0'    #结果保存位置
	app.conf.broker_transport_options = {'fanout_prefix': True}  #默认广播到所有的虚拟用户，设置此项后只发送到指定用户
	app.conf.broker_transport_options = {'fanout_patterns': True} #默认会接受所有的结果，设置此项后只接受相关worker的结果
	app.conf.broker_transport_options = {'visibility_timeout': 43200}  #配置超时时间，持久化任务不受影响
	app.conf.task_serializer = 'json'   #默认使用pickle, 通过此项指定序列化
动态配置文件:
	app.config_from_object('module')  #直接从模块里面加载

#更新多个参数
app.conf.update(
    task_serializer='json',
    accept_content=['json'],  # Ignore other content
    result_serializer='json',
    timezone='Europe/Oslo',
    enable_utc=True,
)
#配置模块celeryconfig.py
	broker_url = 'pyamqp://'
	result_backend = 'rpc://'
	task_serializer = 'json'
	result_serializer = 'json'
	accept_content = ['json']
	timezone = 'Europe/Oslo'
	enable_utc = True
	task_routes = {
  		  'tasks.add': 'low-priority',  #配置路由优先级	 
	}
	task_annotations = {
   		 'tasks.add': {'rate_limit': '10/m'} #限制任务的处理速度, 每分10个
	}

#项目
格局:
    proj/__init__.py
        /celery.py
        /tasks.py
    celery.py:
        from __future__ import absolute_import, unicode_literals
        from celery import Celery
        app = Celery('proj',
                     broker='amqp://',
                     backend='amqp://',
                     include=['proj.tasks'])
       app.conf.update(
             result_expires=3600,
        )
       if __name__ == '__main__':
            app.start()
    tasks.py:
        from __future__ import absolute_import, unicode_literals
        from .celery import app
        @app.task
     def add(x, y):
        return x + y
开启:
    celery -A proj worker -l info



#tasks.py
from celery import Celery
app = Celery('tasks',broker='amqp://', backend='rpc://')
@app.task
def add(x,y):
    return x+y

#执行
from tasks import add
result = add.delay(4,4)
result.ready()  # False or True
result.get(timeout=1) #同步等待，极少使用此命令
result.get(propagate=False)  #当命令抛出异常(raise)时，默认get会重新抛出异常，可以通过此参数控制
result.traceback  #获取任务异常

#queue指定队列， countdonw指定执行时间
add.apply_async((2, 2), queue='lopri', countdown=10)

res.id  #获取结果id