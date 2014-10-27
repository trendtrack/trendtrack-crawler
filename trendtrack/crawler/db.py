# -*- coding:utf-8 -*-
from pymongo.mongo_client import MongoClient
from datetime import datetime


def get_db():
    client = MongoClient()
    db = client.trendtrack
    return db


class JobModel(object):

    def __init__(self,
                 provider,
                 identifier,
                 url,
                 expires_date,
                 publication_date,
                 title,
                 salary,
                 position,
                 company,
                 city,
                 description,
                 tags):
        self.provider = provider
        self.identifier = identifier
        self.url = url
        self.expires_date = expires_date
        self.publication_date = publication_date
        self.title = title
        self.salary = salary
        self.position = position
        self.company = company
        self.city = city
        self.description = description
        self.tags = tags

    def serialize(self):
        return {
            'provider': self.provider,
            'identifier': self.identifier,
            'url': self.url,
            'expires_date': self.expires_date,
            'publication_date': self.publication_date,
            'title': self.title,
            'salary': self.salary,
            'position': self.position,
            'company': self.company,
            'city': self.city,
            'description': self.description,
            'tags': self.tags,
        }

    def save(self):
        db = get_db()
        data = self.serialize()
        job = db.job.find_one({
            'provider': self.provider,
            'identifier': self.identifier
        })
        if job:
            history = job['history']
            history.append({
                'url': job['url'],
                'expires_date': job['expires_date'],
                'publication_date': job['publication_date'],
                'title': job['title'],
                'salary': job['salary'],
                'position': job['position'],
                'company': job['company'],
                'city': job['city'],
                'description': job['description'],
                'tags': job['tags'],
            })
            data.update({
                'update_date': datetime.now(),
                'history': history
            })
            return db.job.update({'_id': job['_id']}, data)
        else:
            data.update({
                'update_date': None,
                'creation_date': datetime.now(),
                'history': []
            })
            return db.job.insert(data)
