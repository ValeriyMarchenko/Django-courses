from django.contrib.auth.models import User
from django.views.generic.edit import CreateView
from django.shortcuts import redirect
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from django.apps import apps
from django.db import models


@login_required
def upgradeAuth(request):
    user = request.user
    premium_group = Group.objects.get(name='author')
    if not request.user.groups.filter(name='author').exists():
        premium_group.user_set.add(user)
        author = apps.get_model('news', 'Author')()
        author.authorUser = user
        author.save()
    return redirect('/')

    
    
