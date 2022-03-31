from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from allauth.account.forms import SignupForm
from django.contrib.auth.models import Group


class BasicSignupForm(SignupForm):
    
    def save(self, commit = True):
        user = super(BasicSignupForm, self).save()
        basic_group = Group.objects.get(name='common')
        basic_group.user_set.add(user)
        return user