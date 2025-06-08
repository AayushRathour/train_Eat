from django.shortcuts import render, get_object_or_404, redirect
from orders.models import Order
from django.contrib import messages

# Create your views here.

def payment_process(request):
    order_id = request.session.get('order_id')
    if not order_id:
        messages.error(request, "No order found to process.")
        return redirect('orders:cart')
        
    order = get_object_or_404(Order, id=order_id)
    
    if request.method == 'POST':
        payment_method = request.POST.get('payment_method')
        
        if payment_method == 'COD':
            order.payment_status = 'COD'
            order.status = 'PREPARING'
            messages.success(request, "Your order has been placed successfully! It will be prepared for cash on delivery.")
        else:
            # Simulate a successful online payment
            order.payment_status = 'PAID'
            order.status = 'PREPARING'
            messages.success(request, "Payment successful! Your order is being prepared.")
            
        order.save()
        
        # Clear the order_id from the session
        del request.session['order_id']
        
        return redirect('payment:done')
    else:
        return render(request, 'payment/process.html', {'order': order})

def payment_done(request):
    return render(request, 'payment/done.html')

def payment_canceled(request):
    order_id = request.session.get('order_id')
    if order_id:
        order = get_object_or_404(Order, id=order_id)
        order.status = 'CANCELLED'
        order.payment_status = 'CANCELLED'
        order.save()
        del request.session['order_id']
    messages.info(request, "Your order has been canceled.")
    return render(request, 'payment/canceled.html')
