import django_filters
from ..models import Product

class ProductFilter(django_filters.FilterSet):
    category__id = django_filters.CharFilter(lookup_expr='iexact')
    category__name = django_filters.CharFilter(lookup_expr='icontains')
    name = django_filters.CharFilter(lookup_expr='icontains')
    description = django_filters.CharFilter(lookup_expr='icontains')
                                                                                    
    class Meta:
        model = Product
        fields = ['category', "category__id", "category__name","name","description"]