import difflib
import re

import tornado
from tornado.httpclient import AsyncHTTPClient

from utils.send_email import SendEmail

client = AsyncHTTPClient()

html_dict = dict()

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}


async def spider():
    table = tornado.ioloop.IOLoop.current().monitor_table
    if not table:
        return None
    for item in table.get('table'):
        if not item.get('switch') or not item.get('url'):
            continue
        try:
            request = tornado.httpclient.HTTPRequest(url=item.get('url'), headers=headers)
            response = await client.fetch(request)
            if response.code != 200:
                print('waring: url:{url}   status_code:{status_code}'.format(url=item.get('url'),
                                                                             status_code=response.code))
                continue
        except Exception as e:
            print('error: {}'.format(e))
        else:
            body = re.match(r'.*(<body>.*</body>)', response.body.decode(), re.S).group(1)
            diff(item.get('url'), body, item.get('email').split(','))


def diff(url, body, email):
    html = html_dict.setdefault(url, {'old_html': body})
    current_html_lines = body.splitlines()
    old_html_lines = html['old_html'].splitlines()
    html_dict[url]['old_html'] = body
    diff_text = ''
    diff_lines = list(difflib.ndiff(old_html_lines, current_html_lines))
    for i in diff_lines:
        if i.startswith('+'):
            diff_text += i[1:]
    if diff_text:
        diff_text.strip()
        print('发送邮件通知')
        SendEmail().send('监控{}有改变'.format(url), diff_text, email)
        print('{url}    {add_content}'.format(url=url, add_content=diff_text))
