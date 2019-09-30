import os

import validators
from tornado.escape import json_decode, json_encode
from tornado.web import RequestHandler
import tornado


class MonitorHandler(RequestHandler):
    def put(self, *args, **kwargs):
        result = {'result': 'ok'}
        table_str = self.request.body.decode()
        table = json_decode(table_str)
        correct_table = {'table': []}
        for item in table.get('table'):
            if validators.url(item.get('url')) and item.get('email'):
                for e in item.get('email').split(','):
                    if not validators.email(e):
                        break
                else:
                    correct_table['table'].append(item)
        if len(table.get('table')) != len(correct_table.get('table')):
            result['result'] = '请检查url或邮箱！！！'

        with open('table.json', 'w', encoding='utf8') as f:
            f.write(json_encode(correct_table))
        tornado.ioloop.IOLoop.current().monitor_table = correct_table
        self.finish(result)

    def get(self, *args, **kwargs):
        if os.path.exists('table.json'):
            with open('table.json', 'r', encoding='utf8') as f:
                table_str = f.read()
                table = json_decode(table_str)
                tornado.ioloop.IOLoop.current().monitor_table = table
                self.finish(table)
        else:
            self.finish({'table': []})
