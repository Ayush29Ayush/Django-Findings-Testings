from celery import shared_task
import logging

logger = logging.getLogger(__name__)

@shared_task
def print_hello():
    logger.info("Hello, World! This is a periodic task.")
    print("Hello, World! This is a periodic task.")
