import logging
from .step import Step


class Postflight(Step):
    def process(self, data, inputs, utils):
        logger = logging.getLogger('yt_concate_log')
        logger.info('in Postflight')
