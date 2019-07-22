import requests
from bs4 import BeautifulSoup
import os
from fetch import Fetch
from tinydb import TinyDB, Query, where

domain = "https://asiansister.com/"
video_page = 15
pic_page = 47

Q = Query()
db_url = TinyDB("db.json")
table_video_url = db_url.table("video")
table_pic_url = db_url.table("pic")
fetch = Fetch()


def get_video_art_list():
    for p in range(1, video_page):
        print("视频第%d页" % p)
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
                "prev_url": prev_url
            }
            if table_video_url.get(where('page_url') == page_url):
                print("重复" + page_url)
            else:
                print(item)
                table_video_url.insert(item)


def get_pic_art_list():
    # pic_art_list = {"pic_url_list": []}
    for p in range(1, pic_page):
        print("图片第%d页" % p)
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
                "prev_url": prev_url
            }
            if table_pic_url.get(where('page_url') == page_url):
                print("重复" + page_url)
            else:
                print(item)
                table_pic_url.insert(item)


def down_video():
    pass


def get_video_meta(page_url):
    res = requests.get(domain + page_url).text
    data = BeautifulSoup(res, "html5lib")
    video_url = data.select("source")[0].attrs['src']
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
        print(img)
        if not os.path.exists("photo/" + page_url):
            os.mkdir("photo/" + page_url)
        photo_url = img.attrs['dataurl'][5:]
        prev_url = img.attrs['data-src']
        img_pack.append({
            "photo_url": photo_url,
            "prev_url": prev_url,
            "flag": 0
        })
        fetch.download_large_file(domain + photo_url, "photo/" + page_url + "/" + photo_url.split("/")[-1])
        fetch.download_large_file(domain + prev_url, "photo/" + page_url + "/" + prev_url.split("/")[-1])

    table_pic_url.update({"flag": 1, "img_pack": img_pack}, where("page_url") == page_url)
    return img_pack


def batch_get_video():
    table_video_url.update({"flag": 0})
    while True:
        item = table_video_url.get(where("flag") == 0)
        if item is None:
            break
        video_url = get_video_meta(item['page_url'])
        fetch.download_large_file(video_url, "mp4/" + item['page_url'] + ".mp4")
        fetch.download_large_file(item['prev_url'], "mp4/" + item['page_url'] + ".jpg")
        table_video_url.update({"flag": 1, "video_url": video_url}, where("page_url") == item['page_url'])


def batch_get_pic():
    # table_pic_url.update({"flag": 0})
    while True:
        if get_pic_meta() is None:
            break


# 获取视频列表
get_video_art_list()
# 获取图包列表
get_pic_art_list()
# 批量获取视频信息
# batch_get_video()
# 批量获取图包信息并下载
batch_get_pic()
