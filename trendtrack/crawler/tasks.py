from celery import Celery

from celery_conf import *


app = Celery('trendtrack.crawler', backend=RESULT_BACKEND,
             broker=BROKER_BACKEND)
