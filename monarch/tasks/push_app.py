from monarch.app import celery
from monarch.utils import logger


@celery.task()
def print_sth():
    logger.debug("任务触发")
