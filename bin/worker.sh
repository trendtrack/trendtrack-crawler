source /usr/local/bin/virtualenvwrapper.sh
workon trendtracker-crawler

celery worker -A trendtrack.crawler.provider.ceviu.tasks -l INFO --concurrency 2