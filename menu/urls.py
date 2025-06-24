from django.urls import path
from . import views

app_name = 'menu'

urlpatterns = [
    path('', views.menu_list, name='menu_list'),
    path('category/<int:category_id>/', views.menu_by_category, name='menu_by_category'),
    path('item/<int:item_id>/', views.menu_item_detail, name='menu_item_detail'),
] 