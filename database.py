# -*- coding: utf-8 -*-

from pymysql import cursors, connect

class DB:
    _db_cursor = None
    _conn = None

    def __init__(self):
        self._host = "xxx.com"
        self._port = 3306
        self._user = "al"
        self._password = "al"
        self._db_name = "al"
        self.connect(self._db_name)
        self.duplicate_count = 0
        self.serial_duplicate_count = 0

    def connect(self, db_name):
        self._db_name = db_name if db_name else ""
        if self._db_name:
            self._conn = connect(self._host,
                                 self._user,
                                 self._password,
                                 db_name,
                                 self._port,
                                 cursorclass=cursors.DictCursor)
            self._conn.autocommit(True)
            self._db_cursor = self._conn.cursor()
        else:
            raise Exception("no database selected")

    def close(self):
        self._db_cursor.close()
        self._conn.close()

    def sql_format(self, d, k):
        if k in d:
            s = d[k]
            if 'str' in str(type(s)):
                s = s.replace("'", "")
                return "'" + s + "'"
            else:
                return s
        else:
            return "NULL"

    def add_photo_pack(self, page_url, prev_url, title):
        try:
            prev_url = prev_url.replace("'", "")
            page_url = page_url.replace("'", "")
            title = title.replace("'", "")
            prev_path = page_url + ".jpg"
            sql = "insert into photo_pack(page_url,prev_url,title,prev_path) " \
                  "values('%s','%s','%s','%s')" \
                  % (page_url,prev_url,title,prev_path)
            self._db_cursor.execute(sql)
            return self._db_cursor.lastrowid
        except Exception:
            raise

    def add_photo_item(self, pack_id, photo_url, prev_url):
        try:
            photo_url = photo_url.replace("'", "")
            prev_url = prev_url.replace("'", "")
            photo_path = photo_url.split("/")[-1]
            prev_path = prev_url.split("/")[-1]
            sql = "insert into " \
                  "photo_item(pack_id, photo_url,prev_url,photo_path,prev_path)" \
                  " values(%d,'%s','%s','%s','%s') " \
                  % (pack_id, photo_url,prev_url,photo_path,prev_path)
            self._db_cursor.execute(sql)
        except Exception:
            raise

    def add_video(self,page_url, prev_url, title, video_url):
        try:
            page_url = page_url.replace("'", "")
            prev_url = prev_url.replace("'", "")
            title = title.replace("'", "")
            video_url = video_url.replace("'", "")
            video_path = page_url + ".mp4"
            prev_path = page_url + ".jpg"
            sql = "insert into video(page_url, prev_url, title, video_url, video_path, prev_path) " \
                  "values('%s','%s','%s','%s','%s','%s') " \
                  % (page_url, prev_url, title, video_url, video_path, prev_path)
            self._db_cursor.execute(sql)
        except Exception:
            raise