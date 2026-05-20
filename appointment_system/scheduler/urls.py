from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('doctors/', views.doctor_list, name='doctors'),

    # Register / Login / Logout
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('logout/', views.logout, name='logout'),

    # Booking System
    path('booking/', views.booking, name='booking'),
    path('mybooking/', views.mybooking, name='mybooking'),

    # Admin Panel
    path('admin-booking/', views.admin_booking, name='admin_booking'),

    # Approve / Reject
    path('approve/<int:id>/', views.approve, name='approve'),
    path('reject/<int:id>/', views.reject, name='reject'),

]
