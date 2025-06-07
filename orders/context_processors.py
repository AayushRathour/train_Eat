from .models import Cart

def cart_item_count(request):
    """
    Makes the cart item count available to all templates.
    """
    if not request.user.is_authenticated:
        return {'cart_item_count': 0}
    
    try:
        cart = Cart.objects.get(user=request.user)
        # Calculate the total number of items by summing their quantities
        count = sum(item.quantity for item in cart.items.all())
    except Cart.DoesNotExist:
        count = 0
        
    return {'cart_item_count': count} 