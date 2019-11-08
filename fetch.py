# -*- coding: utf-8 -*-
from contextlib import closing

import requests
import urllib
from urllib import request
import log
from retry import retry


class Fetch:

    def __init__(self, proxy = None):
        self.__token = None
        self.duplicate_count = 0
        self.serial_duplicate_count = 0
        self.header = {
            "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36",
            "Referer": "https://asiansister.com/"
        }
        self.proxies = proxy

    @retry(stop_max_attempt_number=3,
           stop_max_delay=1000,
           wait_exponential_multiplier=2000,
           wait_exponential_max=6000)
    def download_file(self, url, filename):
        try:
            # create the object, assign it to a variable
            proxy = urllib.request.ProxyHandler(self.proxies)
            # construct a new opener using your proxy settings
            opener = urllib.request.build_opener(proxy)
            # install the openen on the module-level
            urllib.request.install_opener(opener)

            req = request.Request(url, headers=self.header)
            data = request.urlopen(req).read()
            with open(filename, 'wb') as f:
                f.write(data)
                f.flush()
                f.close()
            log.log_info("download finished%s[%s]" % (filename, url))
            return True
        except Exception as e:
            log.log_error(url + str(e))
            raise e

    @retry(stop_max_attempt_number=3,
           stop_max_delay=1000,
           wait_exponential_multiplier=2000,
           wait_exponential_max=6000)
    def download_large_file(self, url, filename):
        count = 0
        try:
            with closing(requests.get(url, proxies=self.proxies, headers=self.header, stream=True, timeout=(5, 20))) as res:
                if 'content-length' not in res.headers:
                    self.download_file(url, filename)
                    return

                chunk_size = 1024000  # 每次请求的块大小
                content_size = int(res.headers['content-length'])  # 文件总大小
                with open(filename, "wb") as file:
                    for data in res.iter_content(chunk_size=chunk_size):
                        count += 1
                        current = chunk_size * count / 1024 / 1024
                        total = content_size / 1024 / 1024
                        log.log_info("total: %.2f MB  current:%.2f MB  percent:%.2f" % (total, current, current/total*100))
                        file.write(data)
            log.log_info("download finished%s[%s]" % (filename, url))
            return True
        except Exception as e:
            log.log_error(url + str(e))
            raise e
