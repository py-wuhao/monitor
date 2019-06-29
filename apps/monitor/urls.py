from tornado.web import url

from .handlers import *
urlpattern = [
    url("/monitor/", MonitorHandler),
]
