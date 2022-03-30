from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
# from .views import BaseRegisterView
from .views import upgradeAuth

urlpatterns = [
    path('logout/', 
         LogoutView.as_view(template_name = 'sign/logout.html'), 
         name='logout'),
    path('upgrade/', upgradeAuth, name = 'upgradeAuth')
]


#     path('login/', 
#          LoginView.as_view(template_name = 'sign/login.html'), 
#          name='login'),
#     path('signup/', 
#          BaseRegisterView.as_view(template_name = 'sign/signup.html'), 
#          name='signup'),