import shutil
import logging
from .step import Step
from yt_concate.settings import DOWNLOADS_DIR


class CleanUP(Step):
    def process(self, data, inputs, utils):
        logger = logging.getLogger('yt_concate_log')
        if inputs['cleanup'] == True:
            shutil.rmtree(DOWNLOADS_DIR)
            logger.info('cleanup the download file')
        else:
            logger.info("Didn't cleanup the download file")