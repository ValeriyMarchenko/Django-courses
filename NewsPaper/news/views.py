from django.shortcuts import render
from django.views.generic import ListView, UpdateView, CreateView, DetailView, DeleteView
from .models import Post
from datetime import datetime
from .filters import PostFilter
from .forms import PostForm

class PostList(ListView):
    model = Post
    template_name = 'posts.html'
    context_object_name = 'posts'
    ordering = '-dateCreation'
    paginate_by = 3

    def get_context_data(self, **kwargs):  
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()
        context['filter'] = PostFilter(self.request.GET, queryset=self.get_queryset()) 
        return context


class PostDetailView(DetailView):
    template_name = 'news/postDetail.html'
    queryset = Post.objects.all()


class PostCreateView(CreateView):
    template_name = 'news/postCreate.html'
    form_class = PostForm


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