from django.urls import path

from . import views

urlpatterns = [
    path('login', views.u_login, name='employee.login'),
    path('logout', views.u_logout, name='employee.logout'),
    path('', views.dashboard, name='employee.dashboard'),
    path('profile', views.profile, name='employee.profile'),
]