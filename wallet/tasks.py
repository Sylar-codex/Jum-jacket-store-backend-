import logging
from huey.contrib.djhuey import db_task

logger = logging.getLogger("huey")

@db_task
def handle_webhook(payload) :
    pass