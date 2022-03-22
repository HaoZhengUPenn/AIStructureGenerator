from django.conf.urls import include, url
from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import PredictView


router = DefaultRouter()#trailing_slash=False)




urlpatterns = [
    path('', include(router.urls)),
    url(r"^(?P<endpoint_name>.+)/predict/$", PredictView.as_view(), name="predict"),

]
