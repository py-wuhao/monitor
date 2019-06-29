from tornado.web import url, StaticFileHandler
from apps.monitor import urls as monitor_urls
from monitor.settings import settings

urlpattern = [
    (url("/view/(.*)", StaticFileHandler, {'path': settings["statics"]}))
]
urlpattern += monitor_urls.urlpattern
