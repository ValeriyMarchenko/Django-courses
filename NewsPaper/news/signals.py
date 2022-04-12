from django.db.models.signals import post_save, pre_save, m2m_changed
from django.dispatch import receiver  # импортируем нужный декоратор
from django.core.mail import EmailMultiAlternatives
from .models import Post
from django.template.loader import render_to_string
import datetime
from django.shortcuts import redirect
from django.contrib.sites.shortcuts import get_current_site


# ---------------MOVED TO CELERY (TASKS.PY)-----------------

# @receiver(m2m_changed, sender=Post.postCategory.through)
# def notify_users_news(sender, instance, action, **kwargs):
#     full_url = ''.join(['http://', get_current_site(None).domain, ':8000'])
#     if action == 'post_add':
#         list_of_subscribers=[]
#         print('11111')
#         for c in instance.postCategory.all():
#             print('222222')
#             print('c')
#             print('instance.postCategory.all()')
#             for usr in c.subscribers.all():
#                 print('333333')
#                 print('c.subscribers.all()')
#                 list_of_subscribers.append(usr)
#         for usr in list_of_subscribers:
#             print('4444444')
#             html_content = render_to_string(
#                 'email/subs_email.html',
#                 {
#                     'post': instance,
#                     'usr': usr,
#                     'full_url': full_url,
#                 }
#             )

#             msg = EmailMultiAlternatives(
#                 subject=instance.title,
#                 body=f'Hey there! New post in  your favourite category!'+instance.text, 
#                 from_email='s44tpdude@yandex.ru',
#                 to=[f'{usr.email}'], 
#             )
#             msg.attach_alternative(html_content, "text/html")  

#             msg.send()  









## m2m_changed.connect(notify_users_news, sender=Post)



#     else:
#         print('5555555')
#         list_of_subscribers = []
#         for c in instance.postCategory.all():
#             print('6666666')
#             for usr in c.subscribers.all():
#                 print('777777')
#                 list_of_subscribers.append(usr)
#         for usr in list_of_subscribers:
#             print('8888888')
#             html_content = render_to_string(
#                 'email/subs_email.html',
#                 {
#                     'post': instance,
#                     'usr': usr,
#                 }
#             )

#             msg = EmailMultiAlternatives(
#                 subject=instance.title,
#                 body=f'Hey! Post in yours favourite category has been edit'+instance.text,  #  это то же, что и message
#                 from_email='s44tpdude@yandex.ru',
#                 to=[f'{usr.email}'], 
#             )
#             msg.attach_alternative(html_content, "text/html") 

#             msg.send()  