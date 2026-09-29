from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard_view, name='pharmacy_dashboard'),
    path('inventory/', views.inventory_list_view, name='pharmacy_inventory'),
    path('inventory/add/', views.inventory_add_view, name='inventory_add'),
    path('inventory/<int:inventory_id>/edit/', views.inventory_edit_view, name='inventory_edit'),
    path('inventory/<int:inventory_id>/delete/', views.inventory_delete_view, name='inventory_delete'),
    path('hours/', views.hours_view, name='pharmacy_hours'),
    path('verification/', views.verification_view, name='pharmacy_verification'),
]
