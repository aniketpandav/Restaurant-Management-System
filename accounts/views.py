from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from .models import Profile
from .forms import UserRegistrationForm

def register(request):
    """
    User registration view
    """
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, f'Account created for {user.username}! You can now login.')
            return redirect('/accounts/login/')
    else:
        form = UserRegistrationForm()
    
    return render(request, 'accounts/register.html', {'form': form})

@login_required
def profile(request):
    """
    User profile view
    """
    return render(request, 'accounts/profile.html')

@login_required
def edit_profile(request):
    """
    Edit user profile view
    """
    try:
        profile = request.user.profile
    except Profile.DoesNotExist:
        profile = Profile.objects.create(user=request.user)
    
    if request.method == 'POST':
        # Update user fields
        user = request.user
        user.first_name = request.POST.get('first_name', '')
        user.last_name = request.POST.get('last_name', '')
        user.email = request.POST.get('email', '')
        user.save()
        
        # Update profile fields
        profile.phone_number = request.POST.get('phone_number', '')
        profile.address = request.POST.get('address', '')
        
        if 'profile_image' in request.FILES:
            profile.profile_image = request.FILES['profile_image']
        
        profile.save()
        messages.success(request, 'Your profile has been updated!')
        return redirect('accounts:profile')
    
    return render(request, 'accounts/edit_profile.html', {'profile': profile})

@login_required
def logout_view(request):
    """
    Custom logout view
    """
    logout(request)
    messages.success(request, 'You have been successfully logged out.')
    return redirect('/')
