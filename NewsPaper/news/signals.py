from django.db.models.signals import post_save, pre_save, m2m_changed
from django.dispatch import receiver  # импортируем нужный декоратор
from django.core.mail import EmailMultiAlternatives
from .models import Post
from django.template.loader import render_to_string
import datetime
from django.shortcuts import redirect
from django.contrib.sites.shortcuts import get_current_site

@receiver(m2m_changed, sender=Post.postCategory.through)
def notify_users_news(sender, instance, action, **kwargs):
    full_url = ''.join(['http://', get_current_site(None).domain, ':8000'])
    if action == 'post_add':
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
                body=f'Здравствуй, {usr.first_name} {usr.last_name}. Новая статья в твоём любимом разделе!'+instance.text,  #  это то же, что и message
                from_email='s44tpdude@yandex.ru',
                to=[f'{usr.email}'],  # это то же, что и recipients_list
            )
            msg.attach_alternative(html_content, "text/html")  # добавляем html

            msg.send()  # отсылаем
    else:
        print('5555555')
        list_of_subscribers = []
        for c in instance.postCategory.all():
            print('6666666')
            for usr in c.subscribers.all():
                print('777777')
                list_of_subscribers.append(usr)
        for usr in list_of_subscribers:
            print('8888888')
            html_content = render_to_string(
                'email/subs_email.html',
                {
                    'post': instance,
                    'usr': usr,
                }
            )

            msg = EmailMultiAlternatives(
                subject=instance.title,
                body=f'Здравствуй. Cтатья в твоём любимом разделе отредактирована!'+instance.text,  #  это то же, что и message
                from_email='s44tpdude@yandex.ru',
                to=[f'{usr.email}'],  # это то же, что и recipients_list
            )
            msg.attach_alternative(html_content, "text/html")  # добавляем html

            msg.send()  # отсылаем

# m2m_changed.connect(notify_users_news, sender=Post)