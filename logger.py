import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

loghandler.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

logger.addHandler(loghandler)
