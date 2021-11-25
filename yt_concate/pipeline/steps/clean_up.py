import shutil
from .step import Step
from yt_concate.settings import DOWNLOADS_DIR


class CleanUP(Step):
    def process(self, data, inputs, utils):
        if inputs['cleanup'] == True:
            shutil.rmtree(DOWNLOADS_DIR)
            print('cleanup the download file')
        else:
            print("Didn't cleanup the download file")