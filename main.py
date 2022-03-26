import argparse
import logging
import sys

import settings
from lib.lf_engine import LoaferEngine
from lib.utils import url_parser, get_vt_siblings


class LOAFER(LoaferEngine):
    def __init__(self, target, debug_level, follow_redirect=True):
        LoaferEngine.__init__(self, target, debug_level, follow_redirect)
        self.rq = self.normal_request()

    def normal_request(self):
        return self.lf_request()

    def custom_request(self, headers=None):
        return self.lf_request(headers=headers)

    def siblings_request(self):
        (hostname, _, path, _, _)=url_parser(self.target)
        self.target = get_vt_siblings(hostname, 10, '40')

        headers = {
            "x-apikey": settings.VT_API_KEY,
            'Accept': 'application/json',
        }
        return self.lf_request(headers=headers)


def calc_logging_level(verbosity):
    default = 40  # errors are printed out
    level = default - (int(verbosity) * 10)
    if level < 0:
        level = 0
    return level


def main():
    # 参数解析
    parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,
                                     description="=====loafer v0.01====="
                                                 "\r\nExample: loafer.py -t http://www.victim.org/")
    parser.add_argument("--target", "-t",
                        dest='target_url',
                        help='target URL')

    parser.add_argument('--version', '-v',
                        action='version',
                        version='%(prog)s version : v 0.01',
                        help='show the version')
    parser.add_argument('--no-redirect',
                        action='store_false',
                        dest='follow_redirect',
                        default=True,
                        help='Do not follow redirections given by 3xx responses')
    parser.add_argument('--verbose',
                        dest='verbose',
                        default=0,
                        help='Enable verbosity, multiple --verbose options increase verbosity')
    parser.add_argument('--debug', '-d',
                        action='store_true',
                        help='show the version',
                        default=False)
    options = parser.parse_args()

    # 引入日志模块
    logging.basicConfig(level=calc_logging_level(options.verbose))
    log = logging.getLogger(__name__)

    print(f'Target Url: {options.target_url}')
    target = options.target_url
    if target is None:
        log.info('Target not given')
        print(f'Example: loafer.py -t http://www.victim.org/')
        sys.exit()
    elif not target.startswith('http'):
        log.info('The url %s should start with http:// or https:// .. fixing (might make this unusable)' % target)
        target = 'https://' + target

    print('[*] Checking {}'.format(target))
    pretty = url_parser(target)
    if pretty is None:
        log.critical('The url %s is not well formed' % target)
        sys.exit(1)
    (hostname, _, path, _, _) = pretty

    # 探测器
    detector = LOAFER(target, debug_level=options.verbose, follow_redirect=options.follow_redirect)
    # 确认用户输入的域名存在
    if detector.rq is None:
        log.error('Site %s appears to be down' % hostname)
    req = detector.siblings_request()
    print (req.text)


#
if __name__ == '__main__':
    main()
