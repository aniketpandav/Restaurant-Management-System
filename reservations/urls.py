from django.urls import path
from . import views

app_name = 'reservations'

urlpatterns = [
    path('', views.reservation_form, name='reservation_form'),
    path('confirm/<int:reservation_id>/', views.reservation_confirm, name='reservation_confirm'),
    path('list/', views.reservation_list, name='reservation_list'),
    path('cancel/<int:reservation_id>/', views.reservation_cancel, name='reservation_cancel'),
] 