from . import views
from django.urls import path


urlpatterns = [
    path('', views.login_user, name='login-user'),
    path('sign-up', views.register, name='register'),
     
]
