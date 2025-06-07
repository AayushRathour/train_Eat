from django.urls import path
from . import views

urlpatterns = [
    path('', views.train_list, name='trains'),
    path('search/', views.train_search, name='train_search'),
    path('<str:train_number>/', views.train_detail, name='train_detail'),
    path('<str:train_number>/route/', views.train_route, name='train_route'),
    path('<str:train_number>/location/', views.train_location, name='train_location'),
    path('stations/', views.station_list, name='stations'),
    path('stations/<str:station_code>/', views.station_detail, name='station_detail'),
    path('stations/<str:station_code>/platforms/', views.platform_list, name='platforms'),
    path('stations/<str:station_code>/platforms/<str:platform_number>/', views.platform_detail, name='platform_detail'),
] 