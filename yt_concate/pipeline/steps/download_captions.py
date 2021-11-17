import os
import time
from threading import Thread

from yt_concate.pipeline.steps.step import Step
from yt_concate.pipeline.steps.step import StepException

from pytube import YouTube


class DownloadCaptions(Step):
    def process(self, data, inputs, utils):
        threads = []
        start = time.time()

        for i in range(4):
            threads.append(Thread(target=self.download_cap, args=(data[i::4], utils)))
        print(threads)

        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()

        end = time.time()
        print('took', end - start, 'seconds')

        return data

    def download_cap(self, data, utils):
        try:
            for yt in data:
                if utils.caption_file_exists(yt):
                    print('found existing caption file')
                    continue
                for caption in YouTube(yt.url).caption_tracks:
                    if caption.name == 'English (auto-generated)':
                        print('download caption for', yt.id)
                        caption = caption.xml_caption_to_srt(caption.xml_captions)
                        text_file = open(yt.get_caption_filepath(), "w", encoding='utf-8')
                        text_file.write(caption)
                        text_file.close()
        except:
            print('Error from pytube')



