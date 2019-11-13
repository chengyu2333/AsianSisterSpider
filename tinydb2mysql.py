from tinydb import TinyDB, Query, where
from database import DB

Q = Query()
db_url = TinyDB("db.json")
table_video_url = db_url.table("video")
table_pic_url = db_url.table("pic")

db = DB()

# video = table_video_url.all()
# for i in video:
#     print(i)
#     if "video_url" in i:
#         db.add_video(i['page_url'], i['prev_url'], i['title'], i['video_url'])

photo = table_pic_url.all()
for i in photo:
    pack_id = db.add_photo_pack(i['page_url'],i['prev_url'],i['title'])
    # break;
    if "img_pack" in i:
        if len(i['img_pack']) == 0:
            print(i)
        for item in i['img_pack']:
            print(item)
            db.add_photo_item(pack_id, item['photo_url'], item['prev_url'])

# pic = table_pic_url.get(where('img_pack') == [])
# print(pic)