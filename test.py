from lib.utils import get_vt_censor
from lib.lf_engine import get_vt_siblings_url

if __name__ == '__main__':
    print(get_vt_censor('40'))
    print(get_vt_siblings_url('www.baidu.com', 40, '70'))
