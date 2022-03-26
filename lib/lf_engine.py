import logging
import time
from copy import copy
import settings
import requests

from lib.utils import get_vt_censor

def_headers = {
    'Accept': 'application/json',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'en-US,en;q=0.9',
    "x-apikey": settings.VT_API_KEY,
    'DNT': '1',  # 服务器不要追踪用户
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3770.100 Safari/537.36',
    'Upgrade-Insecure-Requests': '1'  #
}


def get_vt_siblings(url, limit, index):
    cursor = get_vt_censor(index)
    vt_sb_url = "https://www.virustotal.com/api/v3/domains/" \
                "{}/relationships/siblings?" \
                "limit={}&" \
                "cursor={}".format(url, limit, cursor)
    return vt_sb_url


class LoaferEngine:
    def __init__(self, target='https://www.example.com', debug_level=0, follow_redirect=True, header=None):
        self.follow_redirect = follow_redirect
        self.debug_level = debug_level
        self.target = target
        self.log = logging.getLogger('loafer')
        if header:
            self.headers = header
        else:
            self.headers = copy(def_headers)

    def lf_request(self, headers=None, path=None, params={}, delay=0, timeout=7):
        try:
            time.sleep(delay)
            if not headers:
                h = self.headers
            else:
                h = headers
            self.target = get_vt_siblings('www.baidu.com', 10, '40')
            print(self.target)
            req = requests.get(self.target, proxies=None, headers=h, timeout=timeout,
                               allow_redirects=self.follow_redirect, params=params, verify=False)

            self.log.info('Request Succeeded')
            self.log.info(f'text:{req.text}')
            self.log.debug('Headers: %s\n' % req.headers)
            self.log.debug('Content: %s\n' % req.content)
            return req
        except requests.exceptions.RequestException as e:
            self.log.error('Something went wrong %s' % (e.__str__()))

