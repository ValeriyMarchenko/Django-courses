from django.urls import path
from .views import PostList, PostDetailView, PostCreateView, PostUpdateView, PostDeleteView, PostSearch, UserUpdateView, AddNews, ChangeNews, DeleteNews


urlpatterns = [
    path('', PostList.as_view()),
    # path('<int:pk>', PostDetail.as_view())
    path('<int:pk>/', PostDetailView.as_view(), name='postDetail'),  
    path('create/', AddNews.as_view(), name='postCreate'),  
    path('create/<int:pk>', ChangeNews.as_view(), name='postUpdate'),
    path('delete/<int:pk>', DeleteNews.as_view(), name='postDelete'),
    path('search/', PostSearch.as_view(), name='postSearch'),
    path('http://127.0.0.1:8000/', UserUpdateView.as_view(), name='userUpdate')
]