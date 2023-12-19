

from logging import DEBUG, getLogger, INFO, Logger, StreamHandler
import os

class MetaSingleton(type):
    __instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in MetaSingleton.__instances:
            MetaSingleton.__instances[cls] = super(MetaSingleton, cls).__call__(*args, **kwargs)
        return MetaSingleton.__instances[cls]


class MyLogger(metaclass=MetaSingleton):
    """Logger as a Singleton
    
    """
    def __init__(self):
        self.logger: Logger = getLogger(__name__)
        # create console handler
        ch = StreamHandler()

        if os.getenv("ADVENTOFCODE_DEBUG") == "1":
            self.logger.setLevel(DEBUG)
            ch.setLevel(DEBUG)
        else:
            self.logger.setLevel(INFO)
            ch.setLevel(INFO)
        
        self.logger.addHandler(ch)

    def get_logger(self) -> Logger :
        return self.logger
