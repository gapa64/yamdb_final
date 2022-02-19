from django_filters import CharFilter, FilterSet
from reviews.models import Title


class TitleFilter(FilterSet):
    genre = CharFilter(field_name='genre__slug', lookup_expr='exact')
    category = CharFilter(field_name='category__slug', lookup_expr='exact')
    name = CharFilter(field_name='name', lookup_expr='icontains')

    class Meta:
        model = Title
        fields = ['name', 'year', 'genre', 'category']
