from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from menu.models import MenuItem, Topping

class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('preparing', 'Preparing'),
        ('ready', 'Ready for Pickup'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]
    
    PAYMENT_METHOD_CHOICES = [
        ('cash', 'Cash on Delivery'),
        ('card', 'Credit/Debit Card'),
        ('paypal', 'PayPal'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    address = models.TextField(blank=True)
    phone_number = models.CharField(max_length=15, blank=True)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES, default='cash')
    is_paid = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Order #{self.id} - {self.user.username}"
    
    def update_total(self):
        self.total_price = sum(item.get_total_price() for item in self.items.all())
        self.save()

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.IntegerField(validators=[MinValueValidator(1)], default=1)
    special_instructions = models.TextField(blank=True)
    
    def __str__(self):
        return f'{self.quantity} x {self.menu_item.name}'
    
    def get_total_price(self):
        item_price = self.menu_item.price * self.quantity
        toppings_price = sum(topping.topping.price for topping in self.toppings.all())
        return item_price + toppings_price

class OrderItemTopping(models.Model):
    order_item = models.ForeignKey(OrderItem, on_delete=models.CASCADE, related_name='toppings')
    topping = models.ForeignKey(Topping, on_delete=models.CASCADE)
    
    def __str__(self):
        return f'{self.order_item} - {self.topping.name}'
