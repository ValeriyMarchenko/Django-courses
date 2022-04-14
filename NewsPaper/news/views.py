from django.shortcuts import render
from django.views.generic import ListView, UpdateView, CreateView, DetailView, DeleteView
from .models import *
from datetime import datetime
from .filters import PostFilter
from .forms import PostForm, UserForm
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site

from .tasks import send_mail_for_sub_once
from django.dispatch import receiver
from django.db.models.signals import m2m_changed
from django.core.mail import EmailMultiAlternatives



class PostList(ListView):
    model = Post
    template_name = 'posts.html'
    context_object_name = 'posts'
    ordering = '-dateCreation'
    paginate_by = 3

    
    def get_filter(self):
        return PostFilter(self.request.GET, queryset=super().get_queryset())


    def get_queryset(self):
        return self.get_filter().qs

    
    def get_context_data(self, *args, **kwargs):
        return {
            **super().get_context_data(*args, **kwargs),
            'filter': self.get_filter(),
            'time_now' : datetime.utcnow(),
            'length' : Post.objects.count()
        }


class PostDetailView(DetailView):
    template_name = 'news/postDetail.html'
    queryset = Post.objects.all()


    def get_context_data(self, *args, **kwargs):
        return {
            **super().get_context_data(*args, **kwargs),
            'time_now' : datetime.utcnow(),
        }


class PostCreateView(CreateView):
    template_name = 'news/postCreate.html'
    form_class = PostForm

   
    
    # new_post_notification()
    # subject = 'Created a new post!'
    # content = render_to_string('distribution.html', {'post': Post, })
    # email = request.user.email

    # Отправка уведомлений о новой статье через Celery
    # new_post_notification.delay(subject, email, content)

        


class PostUpdateView(UpdateView):
    template_name = 'news/postCreate.html'
    form_class = PostForm
 
    
    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)


class PostDeleteView(DeleteView):
    template_name = 'news/postDelete.html'
    queryset = Post.objects.all()
    success_url = '/news/'


class PostSearch(ListView):
    model = Post
    template_name = 'postSearch.html'
    context_object_name = 'search'
    ordering = '-dateCreation'

    
    def get_filter(self):
        return PostFilter(self.request.GET, queryset=super().get_queryset())


    def get_queryset(self):
        return self.get_filter().qs

    
    def get_context_data(self, *args, **kwargs):
        return {
            **super().get_context_data(*args, **kwargs),
            'filter': self.get_filter(),
            'time_now' : datetime.utcnow(),
            'length' : Post.objects.count()
        }

class UserUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'news/authorUpdate.html'
    form_class = UserForm
    success_url = '/'

    def get_object(self, **kwargs):
        return self.request.user


class SubscriptionView(ListView):
    model = Category
    template_name = 'subscriptions.html'
    context_object_name = 'subscriptionView'
    queryset = Category.objects.order_by('name')
    paginate_by = 4


@login_required
def add_subscribe(request):
    user = request.user
    print(user)
    category = Category.objects.get(pk=request.POST['id_cat'])
    print(category)
    # subscribe = CategorySubscribers(id_user = user, id_category = category)
    if not category.subscribers.filter(id=user.id).exists():
        
        print(user.id)
        category.subscribers.add(user)
    return redirect('/news/subscriptions/')


@login_required
def end_subscribe(request):
    user = request.user
    print(user)
    category = Category.objects.get(pk=request.POST['id_del'])
    print(category)
    # subscribe = CategorySubscribers(id_user = user, id_category = category)
    if category.subscribers.filter(id=user.id).exists():
        category.subscribers.remove(user)
    return redirect('/news/subscriptions/')


class AddNews(LoginRequiredMixin, PermissionRequiredMixin, PostCreateView):
    permission_required = ('news.add_post',)


class ChangeNews(LoginRequiredMixin, PermissionRequiredMixin, PostUpdateView):
    permission_required = ('news.change_post',)


class DeleteNews(LoginRequiredMixin, PermissionRequiredMixin, PostDeleteView):
    permission_required = ('news.delete_post',)



@receiver(m2m_changed, sender=Post.postCategory.through)
def notify_users_news(instance, action, **kwargs):
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
            user_email = usr.email
            html_content = render_to_string(
                'email/subs_email.html',
                {
                    'post': instance,
                    'usr': usr,
                    'full_url': full_url,
                }
            )

        
        print('start')
        send_mail_for_sub_once.delay(user_email, html_content)
        print('end')
 
