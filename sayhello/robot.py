import requests
import json
import time
import os
import random
# 新视频链接
new_list_api = 'https://api.bilibili.com/x/web-interface/newlist'
# 评论链接
comment_url = 'https://api.bilibili.com/x/v2/reply/add'
# 彩虹屁链接
chp_url = 'https://chp.shadiao.app/api.php'
# 请求头
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.'
                  '146 Safari/537.36'
}
bili_headers = headers.copy()
# cookie文件
cookie_file = 'cookie.txt'
base_data = {
    'oid': '',
    'type': '',
    'message': '',
    'plat:': '1',
    'csrf': 'deef008f0234b6ceb448f52b89270cb4'
}


# 视频评论
def video_comment(message, av):
    data = base_data.copy()
    data['message'] = message
    data['type'] = 1
    data['oid'] = str(av)
    r = requests.post(comment_url, data=data, headers=bili_headers)
    msg = json.loads(r.text)
    if msg['code'] == 0:
        return "发送成功"
    else:
        return msg['message']


# 彩虹屁
def get_chp_sentence():
    return requests.get(chp_url, headers=headers).text


# Robot
class Robot(object):
    @staticmethod
    def new_list_json():
        r = requests.get(new_list_api, headers=headers)
        return json.loads(r.text)

    @staticmethod
    def get_archives():
        return Robot.new_list_json()['data']['archives']

    @staticmethod
    def log(file_name, msg):
        try:
            with open(file_name, 'a') as file:
                file.write(str(msg) + '\n')
                file.flush()
        except Exception as e:
            print("log: ", e)

    base_video_url = 'http://bilibili.com/video/{}'

    def __init__(self):
        self.log_file = 'log.txt'
        self.aid_file = 'avs.txt'
        self.aid_list = []
        self.load_settings()

    # 记录av号
    def log_aid(self, aid):
        Robot.log(self.aid_file, aid)

    # 记录日志
    def log_log(self, log):
        Robot.log(self.log_file, log)

    # 加载访问过的aid
    def load_settings(self):
        try:
            if os.path.isfile(self.aid_file):
                with open(self.aid_file, 'r') as file:
                    self.aid_list.append(file.read().splitlines())
        except Exception as e:
            print("load_settings: ", e)

    def do_something(self):
        try:
            for archive in Robot.get_archives():
                # print(json.dumps(archive, indent=4))
                aid = archive['aid']
                # 访问过的不再重复操作
                if aid in self.aid_list:
                    continue
                self.log_aid(aid)
                self.aid_list.append(aid)
                #
                title = str(archive['title'])
                # tag
                # tag_name = archive['tname']
                # 视频头图
                pic_url = archive['pic']
                # 更新时间
                update = time.strftime("%Y/%m/%d %H:%M:%S", time.localtime(archive['pubdate']))
                # 视频长度
                duration = time.strftime("%M:%S",  time.localtime(archive['duration']))

                owner = archive['owner']
                # 作者id
                owner_id = owner['mid']
                # 作者名字
                owner_name = owner['name']
                # 作者头图
                owner_face = owner['face']
                # bv号
                bvid = archive['bvid']
                url = Robot.base_video_url.format(bvid)
                # 操作
                # 评论内容
                msg = "{}\n{}[doge]".format(duration, get_chp_sentence())
                print(msg)
                rs = video_comment(msg, aid)
                self.log_log("av: {}\ndate: {}\nmsg: {}\nurl: {}\nresult: {}\n\n".format(aid, update, msg, url, rs))
                print(aid, url)

                t = random.randint(1, 9)
                for i in range(t):
                    print('\r剩余:{}s / 共{}s'.format(t - i, t), end='')
                    time.sleep(1)
                print()
        except Exception as e:
            print("do_something: ", e)

    def start(self):
        while True:
            self.do_something()
            time.sleep(2)


def main():
    if os.path.exists(cookie_file):
        try:
            with open(cookie_file, 'r') as file:
                bili_headers['cookie'] = file.read()
        except Exception as e:
            print(e)
    Robot().start()


if __name__ == '__main__':
    main()