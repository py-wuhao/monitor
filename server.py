import os
import time

import tornado
from tornado.escape import json_decode

from monitor.settings import settings
from monitor.urls import urlpattern

from utils.spider import spider

if __name__ == '__main__':
    refresh_interval = 30
    try:
        refresh_interval = int(input('设置刷新间隔(s):'))
    except ValueError:
        print('参数无效，使用默认刷新间隔30s')
    except Exception as e:
        print(e)
        while True:
            time.sleep(3)
    finally:
        print('监控刷新间隔为{}秒'.format(refresh_interval))
        print('操作地址：http://localhost:9999/view/monitor.html')

    app = tornado.web.Application(urlpattern, debug=True, **settings)
    app.listen(9999)
    io_loop = tornado.ioloop.IOLoop.current()
    tornado.ioloop.IOLoop.current().monitor_table = None
    if os.path.exists('table.json'):
        with open('table.json', 'r', encoding='utf8') as f:
            table_str = f.read()
            table = json_decode(table_str)
            tornado.ioloop.IOLoop.current().monitor_table = table
    tornado.ioloop.PeriodicCallback(spider, refresh_interval * 1000).start()
    io_loop.start()
