from orders.models import Order

def cart_processor(request):
    """
    Context processor to add cart information to all templates
    """
    cart_count = 0
    
    if request.user.is_authenticated:
        # Get the current cart if it exists
        cart = Order.objects.filter(user=request.user, status='cart').first()
        if cart:
            cart_count = cart.items.count()
    
    return {
        'cart_count': cart_count
    } 