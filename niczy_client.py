# _*_ coding:utf-8 _*_

import time
import requests

from bs4 import BeautifulSoup


class Niczy(object):

    def __init__(self, ):
        self.user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.124 Safari/537.36"
        self.s = requests.Session()
        self.s.headers["User-Agent"] = self.user_agent
        
    def download(self, url, filename, speed=None, done=None):
        u"""
        :params :speed done multiprocessing Value
        """
        video = self.s.get(url, stream=True, headers={"Range": "bytes=0-"})
        content_length = video.headers["Content-Length"]

        start = time.clock()
        downloaded = 0

        with open(filename, "wb") as f:
            per_start = time.clock()
            for chunk in video.iter_content(1024):
                per_end = time.clock()
                downloaded += 1024
                done.value = float(downloaded) / float(content_length)
                f.write(chunk)
                duration = per_end - per_start
                speed.value = 1 / duration
                per_start = time.clock()        
        total.value = int(time.clock() - start)
        return None

    def video_info(self, url):
        res = self.s.get(url, )
        soup = BeautifulSoup(res.text, "lxml")
        self.soup = soup
        # 名称 系列 图片 关键字
        _dict = {}

        _dict.update(self._other_info(soup))

        _dict[u"series"] = self._series(soup)

        poster_url = _dict["poster_url"]
        _dict["download_url"] = self._download_url(poster_url)

        _dict["video_size"] = self._video_size(_dict["download_url"])

        return _dict

    def _video_size(self, download_url):
        print download_url
        res = self.s.head(download_url)
        length = res.headers["content-length"]
        return length

    def _download_url(self, poster_url):
        import urlparse

        result = urlparse.urlparse(poster_url)
        path = "".join(["/course_def", result.path[16:]])
        url = "".join([result.scheme, "://", result.netloc, path])
        download_url = "".join([url, "_yq.mp4"])
        return download_url

    def _series(self, soup):
        series_list = []
        series = soup.find_all(attrs={"id": "carousel"}) # ul
        if series:
            for li in series[0].find_all("li"):
                url = "".join(["http://niczy.dgut.edu.cn/", li.p.a["href"]])
                name = li.p.a.string
                series_list.append([name, url])
        return series_list

    def _other_info(self, soup):
        p_b_span = []
        info = {}

        lecture_info = soup.find_all(attrs={"class": "lectureInfo"})[0]
        info[u"poster_url"] = lecture_info.img["src"]
        p_b_span.extend(lecture_info.find_all("p"))

        video_info = soup.find_all(attrs={"class": "videoInfo_con"})[0]
        video_p = video_info.find_all("p")
        p_b_span.extend(video_p[:-1])

        name = video_p[-1].string
        info["video_name"] = name[3:] # u"名称：纸牌屋第3季02"

        for p in p_b_span:
            info[p.b.string] = p.span.string

        return info

def mp_downloader(queue, _dict):
    u"""多进程下载
    """
    s = requests.Session()
    s.headers["User-Agent"] = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.124 Safari/537.36"
    while True:
        job = queue.get()
        video = s.get(job["url"], stream=True, headers={"Range": "bytes=0-"})
        content_length = video.headers["Content-Length"]
        start = time.clock()
        downloaded = 0
        with open(job["file_path"], "wb") as f:
            per_start = time.clock()
            for chunk in video.iter_content(1024):
                per_end = time.clock()
                downloaded += 1024
                _dict["done"] = float(downloaded) / float(content_length)
                f.write(chunk)
                duration = per_end - per_start
                _dict["speed"] = 1 / duration
                per_start = time.clock()        
        _dict["total_cost"] = int(time.clock() - start)
    return None

if __name__ == "__main__":
    url = "http://niczy.dgut.edu.cn/index.php?m=content&c=index&a=show&catid=10&id=4488"
    n = Niczy()
    n.video_info(url)
