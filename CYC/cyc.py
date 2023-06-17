import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class Cyc:
    def __init__(self):
        self.session = requests.Session()
        self._search_url = 'https://pc.95189371.cn/video/search'
        self._play_url = 'https://pc.95189371.cn/video/play_url'
        self.headers = {
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) cyc-desktop/1.0.2 Chrome/110.0.5481.208 Electron/23.3.0 Safari/537.36',
        }
        self.session.headers = self.headers
        self._search_result = None

    def __search_video(self):
        keyword = input('搜索动漫：')
        params = {
            'text': keyword,
            'pg': 1,
            'limit': 30
        }
        with self.session.get(self._search_url, params=params, verify=False) as resp:
            self._search_result = resp.json()['data']
            if not self._search_result:
                print('搜索失败，请重新搜索')

    def __choose_video(self):
        names, ids = [], []
        nums = len(self._search_result)
        for item in self._search_result:
            ids.append(item['vod_id'])
            names.append(item['name'])
        for i in range(nums):
            print(f'{i}-------{names[i]}')
        op = int(input('选择影片：'))
        self.video_name = names[op]
        return ids[op]

    def __choose_episode(self, vid):
        params = {
            'id': vid,
            'from': 'cycp'
        }
        with self.session.get(self._play_url, params=params) as resp:
            data = resp.json()['data']
        ep = int(input(f'选择集数(更新至{len(data)}集)：')) - 1
        self.video_name += f' 第{ep+1}集'
        url = data[ep]['url']
        need_parse = data[ep]['needParse']
        if need_parse:
            url = self.__real_url(url)
        return url

    def __real_url(self, url):
        with self.session.get(url, verify=False) as resp:
            result = resp.json()
        real_url = result['url']
        return real_url

    def search(self):
        while not self._search_result:
            self.__search_video()
        vid = self.__choose_video()
        url = self.__choose_episode(vid)
        return url
