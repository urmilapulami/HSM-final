from django.urls import path

from . import views

from .view import room,meal,notice,billing
urlpatterns = [
    path('login', views.u_login, name='student.login'),
    path('logout', views.u_logout, name='admin.logout'),
    path('', views.dashboard, name='student.dashboard'),
    path('profile', views.profile, name='student.profile'),

    
    path('meal', meal.index, name='student.meal'),
    path('room', room.index, name='student.room'),
    path('room/change', room.change, name='student.room_change'),
   
    path('notice', notice.index, name='student.notice'),
    path('billing', billing.index, name='student.billing'),

    
]
