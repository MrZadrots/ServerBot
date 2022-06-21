"""
import logging

def createLogger():
    Log_Format = "%(levelname)s %(asctime)s - %(message)s"
    logging.basicConfig(filename = "logfile.log",
                        filemode = "w",
                        format = Log_Format,
                        level = logging.ERROR)

    logger = logging.getLogger()

    return logger
"""
