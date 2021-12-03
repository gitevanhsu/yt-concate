import time
import logging
from multiprocessing import Process
from pytube import YouTube

from .step import Step

from yt_concate.settings import VIDEOS_DIR


class DownloadVideos(Step):
    def process(self, data, inputs, utils):
        logger = logging.getLogger('yt_concate_log')

        processes = []
        start = time.time()

        for i in range(4):
            processes.append(Process(target=self.download_videos, args=(data[i::4], utils)))
        logger.info(f'{processes}')

        for process in processes:
            process.start()
        for process in processes:
            process.join()

        end = time.time()
        logger.info(f'took {end-start} seconds to download videos')

        return data

    def download_videos(self, data, utils):
        logger = logging.getLogger('yt_concate_log')
        yt_set = set([found.yt for found in data])
        logger.info(f'video to download = {len(yt_set)}')
        for yt in yt_set:
            url = yt.url

            if utils.video_file_exists(yt):
                logger.info(f'found existing file for {url} skipping')
                continue

            logger.info(f'downloading video : {url}')
            YouTube(url).streams.filter(subtype='mp4').first().download(output_path=VIDEOS_DIR, filename=yt.id + '.mp4')


