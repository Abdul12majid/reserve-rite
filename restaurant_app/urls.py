from . import views
from django.urls import path


urlpatterns = [
    path('', views.index, name='index'),
    path('home', views.home_index, name='home_index'),
    path('reserve-rite', views.reserve_index, name='reserve_index'),
    path('book_home_table', views.book_home_table, name='book_home_table'),
    path('book_table', views.book_table, name='book_table'),
    path('reservations', views.reservations, name='reservations'),
    path('about', views.about, name='about'),
    path('contact', views.contact, name='contact'),
    path('profile', views.profile, name='profile'),
    path('details/<int:pk>', views.details, name='details'),
    path('cancel/<int:pk>', views.cancel_reservation, name='cancel'),
    path('edit_reservation/<int:pk>', views.edit_reservation, name='edit'),
     
]

