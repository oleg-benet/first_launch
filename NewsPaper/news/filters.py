from django.forms import DateInput, TextInput
from django_filters import (FilterSet, DateFilter, DateFromToRangeFilter,
                            CharFilter, ModelChoiceFilter)
from django_filters.widgets import RangeWidget
from .models import Post, Author


class PostFilter(FilterSet):
    posted = DateFilter(field_name='post_time', label='Опубликовано после',
                        lookup_expr='gt',
                        widget=DateInput(attrs={'type': 'date'}))
    title = CharFilter(field_name='title', label='Название содержит',
                       lookup_expr='icontains')
    author = ModelChoiceFilter(field_name='author', label='Автор', queryset=Author.objects.all(),
                               empty_label="Выберите из списка")

    class Meta:
        model = Post

        fields = {}
