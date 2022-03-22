from django_filters import rest_framework as filters
from .models import GHRequest

class GHRequestFilter(filters.FilterSet):
    class Meta:
        model = GHRequest
        fields = ('code','gh_num')