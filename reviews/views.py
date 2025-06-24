from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Review
from menu.models import MenuItem

def review_list(request):
    reviews = Review.objects.all()
    
    context = {
        'reviews': reviews,
    }
    
    return render(request, 'reviews/review_list.html', context)

@login_required
def add_review(request):
    if request.method == 'POST':
        menu_item_id = request.POST.get('menu_item')
        rating = int(request.POST.get('rating', 5))
        comment = request.POST.get('comment', '')
        
        menu_item = None
        if menu_item_id:
            menu_item = get_object_or_404(MenuItem, id=menu_item_id)
            
            if Review.objects.filter(user=request.user, menu_item=menu_item).exists():
                messages.error(request, 'You have already reviewed this item')
                return redirect('menu:menu_item_detail', item_id=menu_item_id)
        
        Review.objects.create(
            user=request.user,
            menu_item=menu_item,
            rating=rating,
            comment=comment
        )
        
        messages.success(request, 'Your review has been added successfully!')
        
        if menu_item:
            return redirect('menu:menu_item_detail', item_id=menu_item_id)
        return redirect('reviews:review_list')
    
    menu_items = MenuItem.objects.filter(is_available=True)
    
    menu_item_id = request.GET.get('menu_item')
    menu_item = None
    if menu_item_id:
        menu_item = get_object_or_404(MenuItem, id=menu_item_id)
    
    context = {
        'menu_items': menu_items,
        'menu_item': menu_item,
    }
    
    return render(request, 'reviews/add_review.html', context)

@login_required
def edit_review(request, review_id):
    review = get_object_or_404(Review, id=review_id, user=request.user)
    
    if request.method == 'POST':
        review.rating = int(request.POST.get('rating', 5))
        review.comment = request.POST.get('comment', '')
        review.save()
        
        messages.success(request, 'Your review has been updated successfully!')
        
        if review.menu_item:
            return redirect('menu:menu_item_detail', item_id=review.menu_item.id)
        return redirect('reviews:review_list')
    
    context = {
        'review': review,
    }
    
    return render(request, 'reviews/edit_review.html', context)

@login_required
def delete_review(request, review_id):
    review = get_object_or_404(Review, id=review_id, user=request.user)
    
    if request.method == 'POST':
        menu_item = review.menu_item
        review.delete()
        
        messages.success(request, 'Your review has been deleted successfully!')
        
        if menu_item:
            return redirect('menu:menu_item_detail', item_id=menu_item.id)
        return redirect('reviews:review_list')
    
    context = {
        'review': review,
    }
    
    return render(request, 'reviews/delete_review.html', context)
