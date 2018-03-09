#-*-encoding:utf-8-*-


try:
    from farmconfig import FarmConfig as Config
except ImportError:
    from wikiconfig import Config


sqlrun_storage = Config.sqlrun_storage # 'mongodb'
sqlrun_mongodb_host = Config.sqlrun_mongodb_host # 'localhost'
sqlrun_mongodb_port = Config.sqlrun_mongodb_port # 27017
sqlrun_mongodb_lockdb = Config.sqlrun_mongodb_lockdb # 'sqlrun'
sqlrun_mongodb_lock_coll = Config.sqlrun_mongodb_lock_coll # 'sqlrun_lock'
sqlrun_dbconns = Config.sqlrun_dbconns # {}

# for remote run
from celery import Celery

celeryapp = Celery('sqlrun')
celeryapp.conf.update(
	CELERY_TASK_SERIALIZER='json',
	CELERY_ACCEPT_CONTENT = ['pickle', 'json', 'msgpack', 'yaml'],
	BROKER_URL = 'mongodb://%s:%d/%s' % (sqlrun_mongodb_host, sqlrun_mongodb_port, sqlrun_mongodb_lockdb),
	CELERY_RESULT_BACKEND = 'mongodb://%s:%d/%s' % (sqlrun_mongodb_host, sqlrun_mongodb_port, sqlrun_mongodb_lockdb),
	CELERY_ENABLE_UTC=False,
	USE_TZ = False,
	CELERY_IMPORTS = ('tasks',),#INCLUDE = ('sqlrun.tasks.sql_run_by_worker'),
)
