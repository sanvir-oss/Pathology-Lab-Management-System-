from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    # Home page (your home.html)
    path('', views.home, name='home'),

    # booking (NO test_id in URL now)
    path('book-test/', views.book_test, name='book_test'),
    path('my-bookings/', views.my_bookings, name='my_bookings'),



    # Login / Logout using Django's built-in auth views
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_user, name='logout'),
    # register
    path('register/', views.register, name='register'),



# --- Staff/Admin Paths ---
    path('staff/bookings/', views.admin_bookings, name='admin_bookings'),
    path('staff/manage/<int:booking_id>/', views.manage_booking, name='manage_booking'),


]
