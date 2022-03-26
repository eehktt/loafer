import logging
import re
from urllib.parse import urlparse
import base64

#  封装一个url分析器
import requests
import requests.packages.urllib3


def url_parser(target):
    log = logging.getLogger('urlparser')
    # 禁用关闭认证后的ssl警告
    requests.packages.urllib3.disable_warnings()
    ssl = False
    o = urlparse(target)
    if o[0] not in ['http', 'https', '']:
        log.error('scheme %s not supported' % o[0])
        return
    if o[0] == 'https':
        ssl = True
    if len(o[2]) > 0:
        path = o[2]
    else:
        path = '/'
    tmp = o[1].split(':')
    if len(tmp) > 1:
        port = tmp[1]
    else:
        port = None
    hostname = tmp[0]
    query = o[4]
    return hostname, port, path, query, ssl


def get_title(url):
    result = requests.get(url)
    content = result.text
    try:
        title = re.findall('<title.*>(.*)</title>', content)[0]
    except Exception:
        title = "None"
    return title


def get_vt_censor(index):
    encode_str = "I" + index + "\n."
    return base64.b64encode(bytes(encode_str, 'utf-8')).decode("utf-8")

