from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Order, OrderItem, OrderItemTopping
from menu.models import MenuItem, Topping

@login_required
def cart(request):
    cart, created = Order.objects.get_or_create(
        user=request.user,
        status='cart'
    )
    
    total_price = sum(item.get_total_price() for item in cart.items.all())
    cart.total_price = total_price
    cart.save()
    
    context = {
        'cart': cart,
        'items': cart.items.all(),
    }
    
    return render(request, 'orders/cart.html', context)

@login_required
def add_to_cart(request, item_id):
    menu_item = get_object_or_404(MenuItem, id=item_id, is_available=True)
    
    cart, created = Order.objects.get_or_create(
        user=request.user,
        status='cart'
    )
    
    quantity = int(request.POST.get('quantity', 1))
    
    cart_item = cart.items.filter(menu_item=menu_item).first()
    
    if cart_item:
        cart_item.quantity += quantity
        cart_item.save()
        messages.success(request, f'Increased quantity for {menu_item.name}')
    else:
        special_instructions = ''
        if request.method == 'POST':
            special_instructions = request.POST.get('special_instructions', '')
        
        order_item = OrderItem.objects.create(
            order=cart,
            menu_item=menu_item,
            quantity=quantity,
            special_instructions=special_instructions
        )
        
        if request.method == 'POST':
            topping_ids = request.POST.getlist('toppings')
            for topping_id in topping_ids:
                topping = get_object_or_404(Topping, id=topping_id)
                OrderItemTopping.objects.create(
                    order_item=order_item,
                    topping=topping
                )
        
        messages.success(request, f'{menu_item.name} added to your cart')
    
    cart.update_total()
    
    next_url = request.POST.get('next') or request.GET.get('next')
    if next_url:
        return redirect(next_url)
    
    return redirect('orders:cart')

@login_required
def update_cart(request, item_id):
    order_item = get_object_or_404(OrderItem, id=item_id)
    cart = order_item.order
    
    if cart.user != request.user or cart.status != 'cart':
        messages.error(request, 'You cannot modify this cart')
        return redirect('orders:cart')
    
    quantity = int(request.POST.get('quantity', 1))
    if quantity > 0:
        order_item.quantity = quantity
        order_item.save()
    else:
        order_item.delete()
    
    cart.update_total()
    
    return redirect('orders:cart')

@login_required
def remove_from_cart(request, item_id):
    order_item = get_object_or_404(OrderItem, id=item_id)
    cart = order_item.order
    
    if cart.user != request.user or cart.status != 'cart':
        messages.error(request, 'You cannot modify this cart')
        return redirect('orders:cart')
    
    item_name = order_item.menu_item.name
    order_item.delete()
    
    cart.update_total()
    
    messages.success(request, f'{item_name} removed from your cart')
    return redirect('orders:cart')

@login_required
def checkout(request):
    cart = get_object_or_404(Order, user=request.user, status='cart')
    
    if not cart.items.exists():
        messages.error(request, 'Your cart is empty')
        return redirect('orders:cart')
    
    if request.method == 'POST':
        address = request.POST.get('address', '').strip()
        phone_number = request.POST.get('phone_number', '').strip()
        payment_method = request.POST.get('payment_method', 'cash')
        special_instructions = request.POST.get('special_instructions', '').strip()
        
        if not address:
            messages.error(request, 'Please provide a delivery address')
            return redirect('orders:checkout')
        
        if not phone_number:
            messages.error(request, 'Please provide a phone number')
            return redirect('orders:checkout')
        
        cart.address = address
        cart.phone_number = phone_number
        cart.payment_method = payment_method
        cart.status = 'pending'
        
        if cart.total_price < 50:
            cart.total_price += 5  # Add ₹5 delivery fee
        
        cart.save()
        
        if special_instructions:
            for item in cart.items.all():
                item.special_instructions = special_instructions
                item.save()
        
        messages.success(request, 'Your order has been placed successfully!')
        return redirect('orders:order_confirmation', order_id=cart.id)
    
    context = {
        'cart': cart,
        'user': request.user,
    }
    
    return render(request, 'orders/checkout.html', context)

@login_required
def order_confirmation(request, order_id):
    """
    Order confirmation
    """
    order = get_object_or_404(Order, id=order_id, user=request.user)
    
    context = {
        'order': order,
    }
    
    return render(request, 'orders/order_confirmation.html', context)

@login_required
def order_history(request):
    orders = Order.objects.filter(
        user=request.user
    ).exclude(
        status='cart'
    ).order_by('-created_at')
    
    context = {
        'orders': orders,
    }
    
    return render(request, 'orders/order_history.html', context)

@login_required
def cancel_order(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    
    if order.status not in ['pending', 'preparing']:
        messages.error(request, 'This order cannot be cancelled')
        return redirect('orders:order_history')
    
    order.status = 'cancelled'
    order.save()
    
    messages.success(request, f'Order #{order.id} has been cancelled')
    return redirect('orders:order_history')

@login_required
def reorder(request, order_id):
    original_order = get_object_or_404(Order, id=order_id, user=request.user)
    
    cart, created = Order.objects.get_or_create(
        user=request.user,
        status='cart'
    )
    
    if not created:
        cart.items.all().delete()
    
    for item in original_order.items.all():
        new_item = OrderItem.objects.create(
            order=cart,
            menu_item=item.menu_item,
            quantity=item.quantity,
            special_instructions=item.special_instructions
        )
        
        for topping_item in item.toppings.all():
            OrderItemTopping.objects.create(
                order_item=new_item,
                topping=topping_item.topping
            )
    
    cart.update_total()
    
    messages.success(request, f'Items from order #{original_order.id} have been added to your cart')
    return redirect('orders:cart')
