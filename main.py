import requests
from bs4 import BeautifulSoup
import os
from fetch import Fetch
from tinydb import TinyDB, Query, where
import log

domain = "https://asiansister.com/"
video_page_start = 1
video_page_to = 15
pic_page_start = 1
pic_page_to = 47

Q = Query()
db_url = TinyDB("db.json")
table_video_url = db_url.table("video")
table_pic_url = db_url.table("pic")
fetch = Fetch()

print(len(table_video_url))


def get_video_art_list():
    repeat_count = 0
    for p in range(video_page_start, video_page_to):
        log.log_info("视频第%d页" % p)
        video_url = domain + "video.php?page=%d" % p
        res = requests.get(video_url).text
        data = BeautifulSoup(res, "html5lib")
        box = data.select(".itemBox_video")
        for b in box:
            # print(b)
            page_url = b.select("a")[0].attrs['href']
            title = b.select(".titleName_video")[0].string
            title = title.replace("\n", "")
            title = title.replace("\t", "")
            prev_url = b.attrs['data']
            item = {
                "page_url": page_url,
                "title": title,
                "prev_url": prev_url,
                "flag": 0
            }
            if table_video_url.get(where('page_url') == page_url):
                log.log_info("重复" + page_url)
                repeat_count += 1
                if repeat_count > 10:
                    log.log_success("重复次数达到上线，视频页列表抓取完毕")
                    return
            else:
                print(item)
                table_video_url.insert(item)
    log.log_success("视频页列表抓取完毕")


def get_pic_art_list():
    repeat_count = 0
    for p in range(pic_page_start, pic_page_to):
        log.log_info("图片第%d页" % p)
        pic_url = domain + "_page%d" % p
        res = requests.get(pic_url).text
        data = BeautifulSoup(res, "html5lib")
        box = data.select(".itemBox")
        for b in box:
            page_url = b.select("a")[0].attrs['href']
            title = b.select(".titleName")[0].string
            title = title.replace("\n", "")
            title = title.replace("\t", "")
            prev_url = b.select(".lazyload")[0].attrs['data-src']
            item = {
                "page_url": page_url,
                "title": title,
                "prev_url": prev_url,
                "flag": 0
            }
            if table_pic_url.get(where('page_url') == page_url):
                log.log_info("重复" + page_url)
                repeat_count += 1
                if repeat_count > 10:
                    log.log_success("重复次数达到上线，视频页列表抓取完毕")
                    return
            else:
                print(item)
                table_pic_url.insert(item)
    log.log_success("图片页列表抓取完毕")


def get_video_meta(page_url=None, prev_url=None):
    if page_url is None:
        item = table_video_url.get(where("flag") == 0)
        if item is None:
            return None
        page_url = item['page_url']
        prev_url = domain + item['prev_url']
        print(item)

    res = requests.get(domain + page_url).text
    data = BeautifulSoup(res, "html5lib")
    video_url = data.select("source")[0].attrs['src']
    try:
        fetch.download_large_file(video_url, "video/" + page_url + ".mp4")
        fetch.download_large_file(prev_url, "video/" + page_url + ".jpg")
    except Exception as e:
        log.log_error(str(e))
    table_video_url.update({"flag": 1, "video_url": video_url}, where("page_url") == page_url)
    return video_url


def get_pic_meta(page_url=None):
    if page_url is None:
        item = table_pic_url.get(where("flag") == 0)
        if item is None:
            return None
        page_url = item['page_url']
        print(item)

    res = requests.get(domain + page_url).text
    data = BeautifulSoup(res, "html5lib")
    imgs = data.select(".showMiniImage")
    img_pack = []  # 图包
    for img in imgs:
        if not os.path.exists("photo/" + page_url):
            os.mkdir("photo/" + page_url)
        photo_url = img.attrs['dataurl'][5:]
        prev_url = img.attrs['data-src']
        img_pack.append({
            "photo_url": photo_url,
            "prev_url": prev_url,
            "flag": 0
        })
        try:
            fetch.download_file(domain + photo_url, "photo/" + page_url + "/" + photo_url.split("/")[-1])
            fetch.download_file(domain + prev_url, "photo/" + page_url + "/" + prev_url.split("/")[-1])
        except Exception as e:
            log.log_error(str(e))

    table_pic_url.update({"flag": 1, "img_pack": img_pack}, where("page_url") == page_url)
    return img_pack


def batch_get_video():
    # table_video_url.update({"flag": 0})
    while True:
        if get_video_meta() is None:
            break


def batch_get_pic():
    # table_pic_url.update({"flag": 0})
    while True:
        if get_pic_meta() is None:
            break


# 获取视频列表
get_video_art_list()
# 获取图包列表
get_pic_art_list()
# 批量获取图包信息并下载
batch_get_pic()
# 批量获取视频信息
batch_get_video()

