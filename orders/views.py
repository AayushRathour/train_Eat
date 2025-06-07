from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Order, OrderItem, PNROrder, Cart, CartItem
from vendors.models import FoodItem
from .forms import PNROrderForm, TrackOrderForm, CheckoutForm
from trains.models import Station, Platform
import uuid
from django.conf import settings
from django.utils import timezone
from datetime import timedelta
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction

# Create your views here.

@login_required
def order_list(request):
    """View to display a list of orders for the logged-in user."""
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'orders/order_list.html', {
        'orders': orders
    })

@login_required
def order_detail(request, order_number):
    """View to display details of a specific order."""
    order = get_object_or_404(Order, order_number=order_number, user=request.user)
    return render(request, 'orders/order_detail.html', {
        'order': order
    })

@login_required
def cart(request):
    """View to display the user's shopping cart."""
    cart, created = Cart.objects.get_or_create(user=request.user)
    return render(request, 'orders/cart.html', {'cart': cart})

@login_required
def add_to_cart(request, food_id):
    """View to add a food item to the cart."""
    food_item = get_object_or_404(FoodItem, id=food_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, food_item=food_item)

    if not created:
        cart_item.quantity += 1
        cart_item.save()
        messages.success(request, f'{food_item.name} quantity was updated in your cart.')
    else:
        messages.success(request, f'{food_item.name} was added to your cart.')

    return redirect('vendors:food_list')

@login_required
def remove_from_cart(request, item_id):
    """View to remove an item from the cart."""
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    food_name = cart_item.food_item.name
    cart_item.delete()
    messages.success(request, f'{food_name} has been removed from your cart.')
    return redirect('orders:cart')

@login_required
def update_cart_item(request, item_id):
    """View to update the quantity of an item in the cart."""
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    if request.method == 'POST':
        quantity = request.POST.get('quantity')
        if quantity and quantity.isdigit() and int(quantity) > 0:
            cart_item.quantity = int(quantity)
            cart_item.save()
            messages.success(request, f'Quantity for {cart_item.food_item.name} updated.')
        else:
            messages.error(request, 'Invalid quantity.')
    return redirect('orders:cart')

@login_required
def add_and_checkout(request, food_id):
    """
    Adds a food item to the cart and immediately redirects to the checkout page.
    """
    food_item = get_object_or_404(FoodItem, id=food_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, food_item=food_item)

    if not created:
        cart_item.quantity += 1
        cart_item.save()
        messages.info(request, f'An existing {food_item.name} is in your cart. Its quantity has been updated.')
    else:
        messages.success(request, f'{food_item.name} has been added to your cart.')

    return redirect('orders:checkout')

@login_required
def checkout(request):
    """View to handle the checkout process."""
    cart, created = Cart.objects.get_or_create(user=request.user)
    if not cart.items.exists():
        messages.warning(request, "Your cart is empty. Please add items before checking out.")
        return redirect('vendors:food_list') # Corrected redirect

    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                station_name = form.cleaned_data['delivery_station_name']
                station, _ = Station.objects.get_or_create(name=station_name, defaults={'code': station_name[:4].upper()})
                platform, _ = Platform.objects.get_or_create(station=station, number='1') # Placeholder platform

                order = Order.objects.create(
                    user=request.user,
                    train_id=1,  # Placeholder, should be linked to PNR info
                    delivery_station=station,
                    delivery_platform=platform,
                    order_number=str(uuid.uuid4())[:8].upper(),
                    total_amount=cart.get_total(),
                    special_instructions=form.cleaned_data['special_instructions'],
                    delivery_time=timezone.now() + timedelta(hours=1) # Set delivery time 1 hour from now
                )

                # Move items from cart to order
                for cart_item in cart.items.all():
                    OrderItem.objects.create(
                        order=order,
                        food_item=cart_item.food_item,
                        quantity=cart_item.quantity,
                        price=cart_item.food_item.price
                    )
                
                # Clear the cart
                cart.items.all().delete()
                
                # Redirect to a simple confirmation page instead of payment
                return redirect('orders:order_confirmation', order_number=order.order_number)
    else:
        form = CheckoutForm()

    return render(request, 'orders/checkout.html', {'form': form, 'cart': cart})

@login_required
def order_confirmation(request, order_number):
    """A simple order confirmation page."""
    order = get_object_or_404(Order, order_number=order_number, user=request.user)
    
    # Mark the order as preparing
    order.status = 'PREPARING'
    order.save()
    
    messages.success(request, f"Your order #{order.order_number} has been placed successfully!")
    return render(request, 'orders/order_confirmation.html', {'order': order})

@login_required
def track_order(request, order_number):
    """View to track an order's status."""
    order = get_object_or_404(Order, order_number=order_number, user=request.user)
    return render(request, 'orders/track_order.html', {
        'order': order
    })

@login_required
def cancel_order(request, order_number):
    """View to cancel an order."""
    order = get_object_or_404(Order, order_number=order_number, user=request.user)
    if order.status == 'PENDING':
        order.status = 'CANCELLED'
        order.save()
        messages.success(request, 'Order cancelled successfully!')
    else:
        messages.error(request, 'This order cannot be cancelled.')
    return redirect('orders:order_list')

@login_required
def add_review(request, order_number):
    """View to add a review for an order."""
    order = get_object_or_404(Order, order_number=order_number, user=request.user)
    if request.method == 'POST':
        # TODO: Implement review functionality
        messages.success(request, 'Review added successfully!')
        return redirect('orders:order_detail', order_number=order_number)
    return render(request, 'orders/add_review.html', {
        'order': order
    })

@login_required
def pnr_order(request):
    if request.method == 'POST':
        form = PNROrderForm(request.POST)
        if form.is_valid():
            pnr_order = form.save(commit=False)
            pnr_order.user = request.user
            pnr_order.save()
            messages.success(request, 'PNR order created successfully!')
            return redirect('orders:pnr_order_list')
    else:
        form = PNROrderForm()
    return render(request, 'orders/pnr_order.html', {'form': form})

@login_required
def pnr_order_list(request):
    orders = PNROrder.objects.filter(user=request.user)
    return render(request, 'orders/pnr_order_list.html', {'orders': orders})

def track_order_page(request):
    """
    Displays a form to track an order and shows the result.
    """
    order = None
    form = TrackOrderForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        order_number = form.cleaned_data['order_number']
        phone_number = form.cleaned_data['phone_number']
        
        try:
            order = Order.objects.select_related('user').get(
                order_number__iexact=order_number,
                user__phone_number=phone_number
            )
        except Order.DoesNotExist:
            messages.error(request, 'No order found with the provided details. Please check and try again.')

    return render(request, 'orders/track_order_page.html', {
        'form': form,
        'order': order
    })
