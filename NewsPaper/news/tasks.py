from celery import shared_task
import time
from django.core.mail import EmailMultiAlternatives
from .models import Post
from django.template.loader import render_to_string
import datetime
from django.shortcuts import redirect
from django.contrib.sites.shortcuts import get_current_site


@shared_task
def new_post_notification():
    time.sleep(5)
    full_url = ''.join(['http://', get_current_site(None).domain, ':8000'])
    list_of_subscribers=[]
    print('11111')
    for c in instance.postCategory.all():
        print('222222')
        print('c')
        print('instance.postCategory.all()')
        for usr in c.subscribers.all():
            print('333333')
            print('c.subscribers.all()')
            list_of_subscribers.append(usr)
    for usr in list_of_subscribers:
        print('4444444')
        html_content = render_to_string(
            'email/subs_email.html',
            {
                'post': instance,
                'usr': usr,
                'full_url': full_url,
            }
        )

        msg = EmailMultiAlternatives(
            subject=instance.title,
            body=f'Hey there! New post in  your favourite category!'+instance.text, 
            from_email='s44tpdude@yandex.ru',
            to=[f'{usr.email}'], 
        )
        msg.attach_alternative(html_content, "text/html")  

        msg.send()  