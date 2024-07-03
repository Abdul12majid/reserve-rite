from . import views
from django.urls import path


urlpatterns = [
    path('', views.login_user, name='login-user'),
    path('logout_user', views.logout_user, name='logout-user'),
    path('sign-up', views.register, name='register'),
    path('get_email', views.get_email, name='get_email'),
     
]
