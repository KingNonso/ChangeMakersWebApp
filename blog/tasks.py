import datetime

from django.conf import settings
from django.core.mail import (EmailMultiAlternatives, get_connection,
                              send_mass_mail)
from django.template.loader import render_to_string

from accounts.models import Member
from celery.decorators import periodic_task
from celery.task.schedules import crontab
from celery.utils.log import get_task_logger
from meeting.models import MeetingSchedule

logger = get_task_logger(__name__)


@periodic_task(
    run_every=(crontab(day_of_week="0", hour="12", minute=15)),
    name="send_monthly_reminder_and_newsletter",
    ignore_result=False
)
def send_monthly_reminder_and_newsletter():
    now = datetime.datetime.now() + datetime.timedelta(days=7)
    schedule = MeetingSchedule.schedule()
    if now > schedule:
        send_e_newsletter()
    else:
        pass 


def send_e_newsletter():
    """
    Sends a monthly reminder of the meeting, along with newsletters of the month.

    """
    users = Member.objects.all()
    mailing = []
    schedule = MeetingSchedule.schedule()
    venue = MeetingSchedule.get_venue()
    host = 'http://nse.kingnonso.com' # use django sites framework here

    for u in users:
        mailing += [get_message_for_user(u.user.email, u, schedule, venue, host)]

    now = datetime.datetime.now()
    logger.info("Mail has been sent to all members for  %s"%(now))
    m_tuple = tuple(mailing)
    return send_mass_html_mail(m_tuple, fail_silently=False)



def get_message_for_user(email, user, schedule, venue, host):
    c = {'email': email,
         'user': user,
         'schedule':schedule,
         'venue':venue,
         'host':host}

    day = schedule.strftime("%B %d, %Y")

    email_subject = '%s: Meeting of NSE Abuja '%(day)
    # email_subject = render_to_string(
    #     'blog/email/subject.txt', c).replace('\n', '')
    email_body = render_to_string('blog/email/body.html', c)

    email = (email_subject,
             '',
             email_body,
             settings.DEFAULT_FROM_EMAIL,
             [email]
             )
    return email

'''Modified version of the send mass mail to send html mails'''
def send_mass_html_mail(datatuple, fail_silently=False, user=None, password=None,
                        connection=None):
    """
    Given a datatuple of (subject, text_content, html_content, from_email,
    recipient_list), sends each message to each recipient list. Returns the
    number of emails sent.

    If from_email is None, the DEFAULT_FROM_EMAIL setting is used.
    If auth_user and auth_password are set, they're used to log in.
    If auth_user is None, the EMAIL_HOST_USER setting is used.
    If auth_password is None, the EMAIL_HOST_PASSWORD setting is used.

    """
    connection = connection or get_connection(
        username=user, password=password, fail_silently=fail_silently)
    messages = []
    for subject, text, html, from_email, recipient in datatuple:
        message = EmailMultiAlternatives(subject, text, from_email, recipient)
        message.attach_alternative(html, 'text/html')
        messages.append(message)
    return connection.send_messages(messages)
