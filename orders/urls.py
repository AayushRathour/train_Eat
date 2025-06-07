from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('', views.order_list, name='order_list'),
    path('order/<str:order_number>/', views.order_detail, name='order_detail'),
    path('cart/', views.cart, name='cart'),
    path('add-to-cart/<int:food_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove-from-cart/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('update-cart-item/<int:item_id>/', views.update_cart_item, name='update_cart_item'),
    path('add-and-checkout/<int:food_id>/', views.add_and_checkout, name='add_and_checkout'),
    path('checkout/', views.checkout, name='checkout'),
    path('order-confirmation/<str:order_number>/', views.order_confirmation, name='order_confirmation'),
    path('track-order/<str:order_number>/', views.track_order, name='track_order'),
    path('cancel-order/<str:order_number>/', views.cancel_order, name='cancel_order'),
    path('add-review/<str:order_number>/', views.add_review, name='add_review'),
    path('pnr/', views.pnr_order, name='pnr_order'),
    path('pnr-orders/', views.pnr_order_list, name='pnr_order_list'),
    path('track/', views.track_order_page, name='track_order_page'),
] 