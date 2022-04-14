from celery import shared_task
import time
from django.core.mail import EmailMultiAlternatives
from .models import Post
from django.template.loader import render_to_string
import datetime
from django.shortcuts import redirect
from django.contrib.sites.shortcuts import get_current_site

from django.core.mail import EmailMultiAlternatives
import time
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from news.models import CategorySubscribers, Post
from datetime import datetime, timedelta


@shared_task
def send_mail_for_sub_once(user_mail, html_content):

    msg = EmailMultiAlternatives(
        subject='New Post',
        body=f'Hey there! New post in  your favourite category!', 
        from_email='s44tpdude@yandex.ru',
        to=[f'{user_mail}'], 
        )
    msg.attach_alternative(html_content, "text/html")  

    msg.send()



@shared_task
def weekly_notification():
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