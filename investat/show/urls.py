from django.urls import path
from django.urls.resolvers import URLPattern
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('trans/<int:transaction_id>/', views.transaction_detail, name='detail'),
    path('holdings/', views.holdings, name='holdings'),
    path('holding/<str:ticker>/', views.holding_detail, name='holding'),
    path('dividends/', views.dividends, name='dividends'),
    path('watches/', views.watches, name='watches'),
    path('addrecord/', views.add_record, name='add a record'),
    path('record/submit', views.add_record_submit, name="submit a record")
]