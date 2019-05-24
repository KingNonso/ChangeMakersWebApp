from celery.decorators import task
from celery.utils.log import get_task_logger
from accounts.emails import send_new_user_welcome_email


logger = get_task_logger(__name__)


@task(name="send_new_user_welcome_email_task")
def send_new_user_welcome_email_task(email, user, host):
    """sends an email when a new user has been registered successfully"""
    logger.info("Sent new user successfully registered email")
    return send_new_user_welcome_email(email, user, host)
