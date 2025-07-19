from celery import shared_task
import logging

@shared_task
def print_hello():
    logger = logging.getLogger("celerydummyapp")
    logger.info("Hello, World! This is a periodic task.")
    print("Hello, World! This is a periodic task.")
