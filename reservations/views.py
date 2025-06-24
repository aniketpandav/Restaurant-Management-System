from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Reservation, Table
from datetime import datetime, timedelta

@login_required
def reservation_form(request):
    if request.method == 'POST':
        date_str = request.POST.get('reservation_date')
        time_str = request.POST.get('reservation_time')
        guests = int(request.POST.get('number_of_guests', 1))
        special_request = request.POST.get('special_request', '')
        
        try:
            reservation_date = datetime.strptime(date_str, '%Y-%m-%d').date()
            reservation_time = datetime.strptime(time_str, '%H:%M').time()
            
            reservation = Reservation.objects.create(
                user=request.user,
                reservation_date=reservation_date,
                reservation_time=reservation_time,
                number_of_guests=guests,
                special_request=special_request,
                status='pending'
            )
            
            available_tables = Table.objects.filter(
                is_available=True, 
                capacity__gte=guests
            ).order_by('capacity')
            
            if available_tables.exists():
                reservation.table = available_tables.first()
                reservation.status = 'confirmed'
                reservation.save()
            
            messages.success(request, 'Your reservation has been created! Check your reservations for status updates.')
            return redirect('reservations:reservation_confirm', reservation_id=reservation.id)
        except Exception as e:
            messages.error(request, f'An error occurred: {str(e)}')
    
    available_times = ['18:00', '18:30', '19:00', '19:30', '20:00', '20:30', '21:00', '21:30']
    
    context = {
        'available_times': available_times,
    }
    
    return render(request, 'reservations/reservation_form.html', context)

@login_required
def reservation_confirm(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id, user=request.user)
    
    context = {
        'reservation': reservation,
    }
    
    return render(request, 'reservations/reservation_confirm.html', context)

@login_required
def reservation_list(request):
    reservations = Reservation.objects.filter(user=request.user)
    
    status = request.GET.get('status')
    if status:
        reservations = reservations.filter(status=status)
    
    context = {
        'reservations': reservations,
    }
    
    return render(request, 'reservations/reservation_list.html', context)

@login_required
def reservation_cancel(request, reservation_id):
    reservation = Reservation.objects.get(id=reservation_id, user=request.user)
    if request.method == 'POST':
        reservation.status = 'cancelled'
        reservation.save()
        messages.success(request, 'Your reservation has been cancelled.')
        return redirect('reservations:reservation_list')
    
    context = {
        'reservation': reservation,
    }
    
    return render(request, 'reservations/reservation_cancel.html', context)