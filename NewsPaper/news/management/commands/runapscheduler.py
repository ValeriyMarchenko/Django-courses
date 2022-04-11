import logging
 
from django.conf import settings
 
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.management.base import BaseCommand
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution

from django.core.mail import EmailMultiAlternatives
import time
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from news.models import CategorySubscribers, Post
from datetime import datetime, timedelta


 
 
logger = logging.getLogger(__name__)
 
 
# наша задача по выводу текста на экран
def my_job():
    if CategorySubscribers.objects.all().exists():
        subscribers = CategorySubscribers.objects.all()
        for subscriber in subscribers:
            user = subscriber.id_user
            print(user)
            subject = f'Hey there! Best posts of category: "{subscriber.id_category}" here!'

            postList = Post.objects.filter(dateCreation__gte=(datetime.today() - timedelta(days=7)), postCategory = subscriber.id_category.pk)
            for post in postList:
                print(post.title, post.dateCreation, subscriber.id_category)

            html_content = render_to_string('email/subs_email_each_month.html', {'postList': postList, })
            msg = EmailMultiAlternatives(
                subject=subject,
                body='',
                from_email='s44tpdude@yandex.ru',
                to=[user.email],
            )
            msg.attach_alternative(html_content, "text/html")
            msg.send()
 
 
# функция, которая будет удалять неактуальные задачи
def delete_old_job_executions(max_age=604_800):
    """This job deletes all apscheduler job executions older than `max_age` from the database."""
    DjangoJobExecution.objects.delete_old_job_executions(max_age)
 
 
class Command(BaseCommand):
    help = "Runs apscheduler."
 
    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")
        
        # добавляем работу нашему задачнику
        scheduler.add_job(
            my_job,
            trigger=CronTrigger(month="*/1"),  # То же, что и интервал, но задача тригера таким образом более понятна django
            id="my_job",  # уникальный айди
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'my_job'.")
 
        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="mon", hour="00", minute="00"
            ),  # Каждую неделю будут удаляться старые задачи, которые либо не удалось выполнить, либо уже выполнять не надо.
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )
        logger.info(
            "Added weekly job: 'delete_old_job_executions'."
        )
 
        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")