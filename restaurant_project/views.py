# from django.shortcuts import render
# from menu.models import MenuItem
# from reviews.models import Review

# def home(request):
#     """
#     Home page view showing featured menu items and testimonials
#     """
#     # Get featured menu items
#     featured_items = MenuItem.objects.filter(is_featured=True, is_available=True)[:4]
    
#     # Get testimonials (reviews with highest ratings)
#     testimonials = Review.objects.filter(rating__gte=4)[:3]
    
#     context = {
#         'featured_items': featured_items,
#         'testimonials': testimonials,
#     }
    
#     return render(request, 'home.html', context) 


from django.shortcuts import render
from menu.models import MenuItem
from reviews.models import Review

def home(request):
    featured_items = MenuItem.objects.filter(is_featured=True, is_available=True)[:4]
    
    testimonials = Review.objects.filter(rating__gte=4)[:3]
    
    context = {
        'featured_items': featured_items,
        'testimonials': testimonials,
    }
    
    return render(request, 'home.html', context) 