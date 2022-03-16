from django.views.generic import ListView, DetailView
from .models import Category, Post
from datetime import datetime

class PostList(ListView):
    model = Post
    template_name = 'posts.html'
    context_object_name = 'posts'

    def get_contex_data(self, **kwargs):
        contex = super().get_contex_data(**kwargs)
        context['time_now'] = datetime.utcnow()
        context['value1'] = None
        return contex

class PostDetail(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'