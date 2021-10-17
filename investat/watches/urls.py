from django.urls import path
from django.urls.resolvers import URLPattern
from . import views

urlpatterns = [
    path('', views.index, name='watch index'),
    path('all_etf', views.etf_full_list, name='etf full list'),
]