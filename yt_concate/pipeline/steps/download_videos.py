import time
from multiprocessing import Process
from pytube import YouTube

from .step import Step

from yt_concate.settings import VIDEOS_DIR


class DownloadVideos(Step):
    def process(self, data, inputs, utils):

        processes = []
        start = time.time()

        for i in range(4):
            processes.append(Process(target=self.download_videos, args=(data[i::4], utils)))
        print(processes)

        for process in processes:
            process.start()
        for process in processes:
            process.join()

        end = time.time()
        print('took', end - start, 'seconds to download videos')

    def download_videos(self, data, utils):
        yt_set = set([found.yt for found in data])
        print('video to download = ', len(yt_set))
        for yt in yt_set:
            url = yt.url

            if utils.video_file_exists(yt):
                print('found existing file for', url, ' skipping')
                continue

            print('downloading video :', url)
            YouTube(url).streams.filter(subtype='mp4').first().download(output_path=VIDEOS_DIR, filename=yt.id + '.mp4')

        return data
