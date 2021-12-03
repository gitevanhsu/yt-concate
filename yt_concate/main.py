import sys
import getopt
import logging
from yt_concate.pipeline.steps.preflight import Preflight
from yt_concate.pipeline.steps.get_video_list import GetVideoList
from yt_concate.pipeline.steps.initialize_yt import InitializeYT
from yt_concate.pipeline.steps.download_captions import DownloadCaptions
from yt_concate.pipeline.steps.read_caption import ReadCaption
from yt_concate.pipeline.steps.search import Search
from yt_concate.pipeline.steps.download_videos import DownloadVideos
from yt_concate.pipeline.steps.edit_video import EditVideo
from yt_concate.pipeline.steps.clean_up import CleanUP
from yt_concate.pipeline.steps.postflight import Postflight
from yt_concate.pipeline.steps.step import StepException
from yt_concate.pipeline.pipeline import Pipeline
from yt_concate.utils import Utils


CHANNEL_ID = 'UCKSVUHI9rbbkXhvAXK-2uxA'


def main():
    log_level = logging.WARNING
    inputs = {
        'channel_id': CHANNEL_ID,
        'search_word': 'incredible',
        'limit': 20,
        'cleanup': False,
        'fast': True,
        'log_level': log_level,
    }
    print(sys.argv[1:])

    def print_usage():
        print('main.py OPTIONS')
        print('OPTIONS')
        print('--channel <channel_id>'
              '--search <search word>'
              '--limit <limit number>'
              'fast <Ture/False>'
              'cleanup <Ture/False>'
              'log <DEBUG/INFO/WARNING/ERROR/CRITICAL>')

        print('{:>6} {:<12}{}'.format('-c', '--channel', 'channel id on Youtube'))
        print('{:>6} {:<12}{}'.format('-s', '--search', 'search word in videos'))
        print('{:>6} {:<12}{}'.format('-l', '--limit', 'limit videos of edit'))
        print('{:>6} {:<12}{}'.format('', '--fast', 'ignore step when file existing'))
        print('{:>6} {:<12}{}'.format('', '--cleanup', 'remove all downloads'))
        print('{:>6} {:<12}{}'.format('', '--log', 'select log level to print on cmd'))

    def input_argument():
        short_otp = 'hc:s:l:f:'
        long_opt = 'help cleanup channel= search= limit='.split()

        try:
            opts, args = getopt.getopt(sys.argv[1:], short_otp, long_opt)
        except getopt.GetoptError:
            print_usage()
            sys.exit(2)

        print(opts, '\n', args)

        for opt, arg in opts:
            if opt == '-h':
                print_usage()
                sys.exit(0)
            elif opt in ("-c", "--channel"):
                inputs['channel_id'] = arg
            elif opt in ("-s", "--search"):
                inputs['search_word'] = arg
            elif opt in ("-l", "--limit"):
                inputs['limit'] = arg
            elif opt in ("-f", "--fast"):
                if arg == bool(arg):
                    inputs['fast'] = True
            elif opt == 'cleanup':
                inputs['cleanup'] = True
            elif opt == 'log':
                inputs['log_level'] = eval(f'logging.{arg}')

    input_argument()

    steps = [
        Preflight(),
        GetVideoList(),
        InitializeYT(),
        DownloadCaptions(),
        ReadCaption(),
        Search(),
        DownloadVideos(),
        EditVideo(),
        CleanUP(),
        Postflight(),
    ]

    utils = Utils()
    p = Pipeline(steps)
    p.run(inputs, utils)


if __name__ == '__main__':
    main()
