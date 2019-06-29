import sys
import time
import difflib

import requests

monitor_url = 'https://www.nuedc-training.com.cn/'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'
}
last_html = None
while True:
    res = requests.get(url=monitor_url, headers=headers, verify=False)
    if res.status_code == 200:
        current_html = res.text
        if last_html:
            current_html_lines = current_html.splitlines()
            last_html_lines = last_html.splitlines()
            diff_text = ''
            diff = list(difflib.ndiff(last_html_lines, current_html_lines))
            for i in diff:
                if i.startswith('+'):
                    diff_text += i[1:]
            print(diff_text)
        last_html = current_html
    time.sleep(3)
