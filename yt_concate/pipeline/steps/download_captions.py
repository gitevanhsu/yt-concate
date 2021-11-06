
import os
import time

import requests
import youtube_dl.utils
from youtube_dl import YoutubeDL

from yt_concate.pipeline.steps.step import Step
from yt_concate.pipeline.steps.step import StepException


class DownloadCaptions(Step):
    def process(self, data, inputs, utils):
        start = time.time()
        for url in data:
            print("downloading caption for", url)
            if utils.caption_file_exists(url):
                print('found existing caption file')
                continue
            try:
                ydl = YoutubeDL({'writesubtitles': True, 'allsubtitles': True, 'writeautomaticsub': True})
                res = ydl.extract_info(url, download=False)
                if res['requested_subtitles'] and res['requested_subtitles']['en']:
                    # print('Grabbing vtt file from ' + res['requested_subtitles']['en']['url'])
                    response = requests.get(res['requested_subtitles']['en']['url'], stream=True)
                    # print(response.text)

                    f1 = open(utils.get_caption_filepath(url), "w", encoding='utf-8')
                    f1.write(response.text)
                    f1.close()

                    if len(res['subtitles']) > 0:
                        print('manual captions')
                    else:
                        print('automatic_captions')
                else:
                    print('Youtube Video does not have any english captions')
            except (KeyError, AttributeError, youtube_dl.utils.DownloadError):
                print('Error when downloading caption for', url)
                continue

        end = time.time()
        print('took', end - start, 'seconds')









