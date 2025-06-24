from django.shortcuts import render, get_object_or_404
from .models import MenuItem, Category

def menu_list(request):

    categories = Category.objects.all()
    menu_items = MenuItem.objects.filter(is_available=True).order_by('category__name', 'name')
    
    category_id = request.GET.get('category')
    if category_id:
        menu_items = menu_items.filter(category_id=category_id)
    
    context = {
        'categories': categories,
        'menu_items': menu_items,
        'current_category': category_id,
    }
    
    return render(request, 'menu/menu_list.html', context)

def menu_by_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    categories = Category.objects.all()
    menu_items = MenuItem.objects.filter(category=category, is_available=True).order_by('name')
    
    context = {
        'category': category,
        'categories': categories,
        'menu_items': menu_items,
        'current_category': category_id,
    }
    
    return render(request, 'menu/menu_list.html', context)

def menu_item_detail(request, item_id):
    menu_item = get_object_or_404(MenuItem, id=item_id, is_available=True)
    related_items = MenuItem.objects.filter(
        category=menu_item.category, 
        is_available=True
    ).exclude(id=item_id)[:4]
    
    context = {
        'menu_item': menu_item,
        'related_items': related_items,
    }
    
    return render(request, 'menu/menu_item_detail.html', context)
