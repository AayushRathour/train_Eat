from django.urls import path
from . import views

app_name = 'vendors'

urlpatterns = [
    path('search/', views.search, name='search'),
    path('', views.vendor_list, name='vendors'),
    path('<int:vendor_id>/', views.vendor_detail, name='vendor_detail'),
    path('<int:vendor_id>/menu/', views.vendor_menu, name='vendor_menu'),
    path('<int:vendor_id>/reviews/', views.vendor_reviews, name='vendor_reviews'),
    path('food/<int:food_id>/', views.food_detail, name='food_detail'),
    path('foods/', views.food_list, name='food_list'),
    path('categories/', views.category_list, name='categories'),
    path('categories/<int:category_id>/', views.category_detail, name='category_detail'),
] 