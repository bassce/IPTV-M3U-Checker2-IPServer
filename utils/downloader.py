#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Time    : 2024/04/17 00:50
# @Author  : Allen zh
# @Email   : allenzh@outlook.com
# @File    : downloader.py

import time
from urllib.request import urlopen
try:
    import cv2
    _g_CV2 = True
except ImportError:
    _g_CV2 = False

class Downloader:
    def __init__(self, url, m3url=None):
        self.url = url
        self.startTime = time.time()
        self.receive = 0
        self.endTime = None
        self.m3url = m3url

    def getSpeed(self):
        if self.endTime and self.receive != -1:
            return self.receive / (self.endTime - self.startTime)
        else:
            return -1

    def downloadTester(self, retry):
        chunk_size = 10240
        for i in range(retry):
            try:
                resp = urlopen(self.url, timeout=2)
                while time.time() - self.startTime < 5:
                    chunk = resp.read(chunk_size)
                    if not chunk:
                        break
                    self.receive += len(chunk)
                resp.close()
                break
            except Exception as e:
                print(f"downloadTester encountered an error {e}, retry {i+1}, {self.m3url}")
                self.receive = -1 # 标记失败
                self.startTime = time.time() # 重置开始时间
                if i == retry - 1:  # 如果达到最大重试次数，跳出循环
                    print(f"Max retries reached for URL: {self.m3url}")
        self.endTime = time.time()

    def getVideoFormat(self):
        video_url = self.url
        width = 0
        height = 0
        cformat = "NaN"

        if len(video_url) > 0:
            try:
                video = cv2.VideoCapture(video_url)
                if video.isOpened():
                    width = video.get(cv2.CAP_PROP_FRAME_WIDTH)
                    height = video.get(cv2.CAP_PROP_FRAME_HEIGHT)
                    frcc = int(video.get(cv2.CAP_PROP_FOURCC))
                    cformat = f"{chr(frcc & 0xFF)}{chr((frcc & 0xFF00) >> 8)}{chr((frcc & 0xFF0000) >> 16)}{chr((frcc & 0xFF000000) >> 24)}"
                    video.release()
                if width == 0 or height == 0:
                    print(f"Warning: Detected 0*0 resolution for {video_url}")
            except Exception as e:
                print(f"Error retrieving video format: {e}")
        return width, height, cformat

def getStreamUrl(m3u8):
    urls = []
    if not m3u8.lower().endswith('.m3u8'):
        return [m3u8]
    try:
        prefix = m3u8[:m3u8.rindex('/') + 1]
        with urlopen(m3u8, timeout=5) as resp:
            top, second = False, False
            firstLine = True
            for line in resp:
                line = line.decode('utf-8').strip()
                if firstLine:
                    firstLine = False
                    if line != '#EXTM3U':
                        return [m3u8]
                if top:
                    line = prefix + line if not line.lower().startswith('http') else line
                    urls += getStreamUrl(line)
                    top = False
                if second:
                    line = prefix + line if not line.lower().startswith('http') else line
                    urls.append(line)
                    second = False
                if line.startswith('#EXT-X-STREAM-INF:'):
                    top = True
                if line.startswith('#EXTINF:'):
                    second = True
    except Exception as e:
        print(f'Failed to get stream url: {e}')
    return urls

def start(url, bChkFormat=False, retry=3):
    stream_urls = getStreamUrl(url) if not url.lower().endswith('.flv') else [url]
    speed, width, height, cformat = -1, 0, 0, "NaN"
    if stream_urls:
        downloader = Downloader(stream_urls[0], url)
        if bChkFormat:
            width, height, cformat = downloader.getVideoFormat()
        downloader.downloadTester(retry)
        speed = downloader.getSpeed()
    return speed, width, height, cformat
