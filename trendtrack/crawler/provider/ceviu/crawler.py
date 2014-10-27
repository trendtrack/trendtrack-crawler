# -*- coding:utf-8 -*-
import xml.etree.ElementTree as ET
from datetime import datetime

import requests
from BeautifulSoup import BeautifulSoup

from trendtrack.crawler import db
from trendtrack.crawler.utils import encode_str

from .settings import SITEMAP_URL, PROVIDER_CODE


class Crawler(object):

    def __init__(self):
        self.db = db.get_db()

    def get_all_jobs(self, callback):
        sitemap = self._get_sitemap()
        identifiers = []

        parser = ET.fromstring(sitemap)
        items = parser.getchildren()

        for item in items[1:30]:
            sub_items = item.getchildren()
            url = sub_items[0].text
            identifier = url.split('-')[-1]

            if identifier in identifiers:
                continue

            if self._check_if_exists(identifier):
                continue

            identifiers.append(identifier)
            data = {
                'provider': PROVIDER_CODE,
                'url': url,
                'identifier': identifier
            }
            callback(data)

    def get_job_page_content(self, data, callback):
        response = requests.get(data['url'])

        if response.status_code != 200:
            raise Exception("Invalid status '{}'".format(response.status_code))

        data['page_content'] = response.text
        object_id = self.db.pending_job.insert(data)
        callback(object_id)

    def get_job_detail(self, object_id):
        data = self.db.pending_job.find_one({'_id': object_id})
        parser = BeautifulSoup(data['page_content'])
        detail = self._parse_job_detail(parser)

        job = db.JobModel(
            provider=data['provider'],
            identifier=data['identifier'],
            url=data['url'],
            expires_date=detail['expires_date'],
            publication_date=detail['publication_date'],
            title=detail['title'],
            salary=detail['salary'],
            position=detail['position'],
            company=detail['company'],
            city=detail['city'],
            description=detail['description'],
            tags=detail['tags']
        )
        job.save()
        self.db.pending_job.remove({'_id': object_id})
        return job

    def _parse_job_detail(self, parser):
        parser = parser.find('div', id='boxVaga')

        values = parser.findAll('div', {'id': 'direitaD'})
        keys = parser.findAll('div', {'id': 'esquerdaD'})
        keys = [encode_str(x.text)[:-1].lower() for x in keys]

        data = {}
        for i, x  in enumerate(keys):
            data[x] = values[i].renderContents().strip()

        publication_date = parser.find('div', {'id': 'direita'}).text
        index = publication_date.index('Data:')+5
        publication_date = publication_date[index:index+10]
        publication_date = datetime.strptime(publication_date, '%d/%m/%Y')

        return {
            'expires_date': None,
            'publication_date': publication_date,
            'title': parser.find('span', {'class': 'tituloVaga'}).text,
            'salary': data.get('salario'),
            'position': data.get('cargo'),
            'company': None,
            'city': data.get('cidade'),
            'description': data['descricao'],
            'tags': []
        }

    def _check_if_exists(self, identifier):
        pending_job = self.db.pending_job.find({'identifier': identifier})
        job = self.db.job.find({
            'identifier': identifier,
            'provider': PROVIDER_CODE
        })
        return pending_job.count() or job.count()

    def _get_sitemap(self):
        return requests.get(SITEMAP_URL).content
