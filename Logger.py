import logging

logger = logging.getLogger()
ch = logging.StreamHandler()
formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s",'%y%m%d %H%M%S')
ch.setFormatter(formatter)
logger.addHandler(ch)
