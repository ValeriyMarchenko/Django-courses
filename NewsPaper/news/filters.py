from django_filters import FilterSet, DateFilter, CharFilter
from .models import Post
from datetime import datetime
import django
import django_filters

class PostFilter(FilterSet):
    dateCreation = DateFilter(
        label = 'Date',
        lookup_expr='gt',
        widget=django.forms.DateInput(
            attrs={
                'type': 'date'
            }
        )
    )
    dateCreation.field.error_messages = {'invalid' : 'Input date in format: DD.MM.YYYY. Example: 05.02.2022'}
    dateCreation.field.widget.attrs = {'placeholder' : 'DD.MM.YYYY'}


    class Meta:
        model = Post
        fields = {
            'title': ['icontains'],
            'author': ['exact'],
            'categoryType': ['exact'],
            
        }


# date = django_filters.DateFilter(
#         field_name="create_time",
#         lookup_expr="gte",
#         label="Date:",
#         )
