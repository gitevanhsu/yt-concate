import os
import time

import requests
import youtube_dl.utils
from youtube_dl import YoutubeDL

from yt_concate.pipeline.steps.step import Step
from yt_concate.pipeline.steps.step import StepException
from yt_concate.utils import CAPTIONS_DIR


class DownloadCaptions(Step):
    def process(self, data, inputs, utils):
        start = time.time()
        for url in data:
            print('downloading caption for', utils.get_video_id_from_url(url))
            if utils.caption_file_exists(url):
                print('found existing caption file')
                continue

            ydl_opt = {
            'skip_download': True,
            'writesubtitles': True,
            'writeautomaticsub': True,
            'subtitleslangs': ['en'],
            'outtmpl': utils.get_caption_filepath(url),
            'nooverwrites': False,
            }

            try:
                with YoutubeDL(ydl_opt) as ydl:
                    print(ydl.download([url]))

            except Exception as e:
                print(e)
                print("An Error occur for", url)
                continue

        end = time.time()
        print('took', end - start, 'seconds')










