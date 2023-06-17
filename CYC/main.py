import os

import tqdm

from cyc import Cyc
from download import Downloader


def download_with_m3u8():
    global cyc, url
    with cyc.session.get(url, verify=False) as resp:
        filename = cyc.video_name + '.m3u8'
        with open(filename, mode='w') as f:
            f.write(resp.text)
    filepath = os.getcwd() + '/' + filename
    downloader = Downloader(filepath)
    downloader.download(skip_fake_head=471)


def download_with_aria2():
    global url
    import aria2p
    aria2 = aria2p.API(
        aria2p.Client(
            host="http://localhost",
            port=6800,
            secret=""
        )
    )
    aria2.add(uri=url)
    print('已成功发送至aria2')


def download_with_requests():
    global cyc, url
    with cyc.session.get(url=url, stream=True) as resp:
        size = int(resp.headers.get('content-length', 0))
        chunk = 1024
        with open(f'{cyc.video_name}.mp4', mode='wb') as f:
            with tqdm.tqdm(total=size, unit='B', unit_scale=True) as bar:
                for data in resp.iter_content(chunk_size=chunk):
                    f.write(data)
                    bar.update(len(data))


if __name__ == '__main__':
    cyc = Cyc()
    url = cyc.search()
    print(url)
    if url.split('.')[-1] == 'm3u8':
        download_with_m3u8()
    else:
        try:
            download_with_aria2()
        except Exception as e:
            print(e)
            print('切换至本地下载')
            download_with_requests()
