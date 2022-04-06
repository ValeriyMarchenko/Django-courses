from django.urls import path
from .views import *


urlpatterns = [
    path('', PostList.as_view()),
    # path('<int:pk>', PostDetail.as_view())
    path('<int:pk>/', PostDetailView.as_view(), name='postDetail'),  
    path('create/', AddNews.as_view(), name='postCreate'),  
    path('create/<int:pk>', ChangeNews.as_view(), name='postUpdate'),
    path('delete/<int:pk>', DeleteNews.as_view(), name='postDelete'),
    path('search/', PostSearch.as_view(), name='postSearch'),
    path('profile/', UserUpdateView.as_view(), name='userUpdate'),
    path('subscriptions/', SubscriptionView.as_view()),
    path('subscriptions/subscribe', add_subscribe, name = 'subscribe'),
    path('subscriptions/unsubscribe', end_subscribe, name = 'unsubscribe'),
]