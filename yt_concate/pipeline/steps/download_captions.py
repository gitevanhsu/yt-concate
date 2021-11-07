import os
import time

from yt_concate.pipeline.steps.step import Step
from yt_concate.pipeline.steps.step import StepException

from pytube import YouTube

class DownloadCaptions(Step):
    def process(self, data, inputs, utils):
        start = time.time()

        for url in data:
            try:
                source = YouTube(url)
                caption = source.captions.get_by_language_code('a.en')
                en_caption_convert_to_srt = caption.generate_srt_captions()
                print(en_caption_convert_to_srt)

                text_file = open(utils.get_caption_filepath(url), "w", encoding='utf-8')
                text_file.write(en_caption_convert_to_srt)
                text_file.close()
            except (KeyError, AttributeError):
                print("an Error for :", url)
                continue

        end = time.time()
        print('took', end - start, 'seconds')

