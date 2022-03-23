from django.urls import path
from .views import PostList, PostDetailView, PostCreateView, PostUpdateView, PostDeleteView, PostSearch


urlpatterns = [
    path('', PostList.as_view()),
    # path('<int:pk>', PostDetail.as_view())
    path('<int:pk>/', PostDetailView.as_view(), name='postDetail'),  
    path('create/', PostCreateView.as_view(), name='postCreate'),  
    path('create/<int:pk>', PostUpdateView.as_view(), name='postUpdate'),
    path('delete/<int:pk>', PostDeleteView.as_view(), name='postDelete'),
    path('search/', PostSearch.as_view(), name='postSearch')
]