# -*- coding:utf-8 -*-
import unittest
import os.path

from mock import Mock

from trendtrack.crawler.provider.ceviu.crawler import Crawler


def get_mockup(filename):
    current_dir = os.path.dirname(os.path.realpath(__file__))
    location = os.path.join(current_dir, 'mockup/{}'.format(filename))
    return open(location, 'r')


class GetAllJobsTest(unittest.TestCase):

    def setUp(self):
        self.crawler = Crawler()
        with get_mockup('sitemap.xml') as sitemap:
            self.crawler._get_sitemap = Mock(return_value=sitemap.read())

    def test_get_all_jobs(self):
        expected_urls = [{
                'identifier': '1000',
                'provider': 'ceviu',
                'url': 'http://www.ceviu.com.br/buscar/vaga/emprego-1000'
            },
            {
                'identifier': '2000',
                'provider': 'ceviu',
                'url': 'http://www.ceviu.com.br/buscar/vaga/emprego-2000'
            }
        ]
        urls = []
        callback = lambda x: urls.append(x)

        self.crawler.get_all_jobs(callback)

        for expected_url in expected_urls:
            self.assertTrue(expected_url in urls)
