# -*- coding:utf-8 -*-
from time import sleep
from datetime import timedelta
from celery import task
from pymongo.mongo_client import MongoClient
import requests

from trendtrack.crawler.tasks import app

from trendtrack.crawler.provider.ceviu.crawler import Crawler
from settings import REQUEST_INTERVAL


crawler = Crawler()


@app.task
def get_all_jobs():
    crawler.get_all_jobs(callback=get_job_page_content.delay)


@app.task(bind=True, default_retry_delay=REQUEST_INTERVAL * 10)
def get_job_page_content(self, data):
    try:
        sleep(REQUEST_INTERVAL)
        crawler.get_job_page_content(data, callback=get_job_detail.delay)
    except Exception as exc:
        raise self.retry(exc=exc)


@app.task
def get_job_detail(object_id):
    crawler.get_job_detail(object_id)
