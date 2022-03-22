from django_filters import FilterSet, DateFilter
from .models import Post
from datetime import datetime
import django

class PostFilter(FilterSet):
    class Meta:
        model = Post
        dateCreation = DateFilter(
        lookup_expr='icontains',
        widget=django.forms.DateInput(
            attrs={
                'type': 'date'
            }
        )
    )
        fields = {
            'dateCreation': ['gt'],
            'title': ['icontains'],
            "author": ['in'],
        }