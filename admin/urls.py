from django.urls import path


from . import views
from .view import hostel,room,meal,notice,billing


urlpatterns = [
    path('login', views.u_login, name='admin.login'),
    path('logout', views.u_logout, name='admin.logout'),
    path('', views.dashboard, name='admin.dashboard'),
    path('profile', views.profile, name='admin.profile'),

    path('student', views.student, name='admin.student'),
    path('student/add', views.student_add, name='admin.student_add'),
    path('student/activate/<int:id>', views.student_activete, name='admin.student_activete'),
    path('student/deactivete/<int:id>', views.student_deactivete, name='admin.student_deactivete'),
    path('student/edit/<int:id>', views.student_edit, name='admin.student_edit'),
    path('student/view/<int:id>', views.student_view, name='admin.student_view'),

    
    path('employee', views.employee, name='admin.employee'),
    path('employee/add', views.employee_add, name='admin.employee_add'),
    path('employee/activate/<int:id>', views.employee_activete, name='admin.employee_activete'),
    path('employee/deactivete/<int:id>', views.employee_deactivete, name='admin.employee_deactivete'),
    path('employee/edit/<int:id>', views.employee_edit, name='admin.employee_edit'),

      
    path('admin', views.admin, name='admin.admin'),
    path('admin/add', views.admin_add, name='admin.admin_add'),
    path('admin/activate/<int:id>', views.admin_activete, name='admin.admin_activete'),
    path('admin/deactivete/<int:id>', views.admin_deactivete, name='admin.admin_deactivete'),
    path('admin/edit/<int:id>', views.admin_edit, name='admin.admin_edit'),

    
    path('hostel', hostel.index, name='admin.hostel'),
    path('hostel/add', hostel.add, name='admin.hostel_add'),
    path('hostel/edit/<int:id>', hostel.edit, name='admin.hostel_edit'),

    path('hostel', hostel.index, name='admin.hostel'),
    path('hostel/add', hostel.add, name='admin.hostel_add'),
    path('hostel/rooms/<int:h_id>', room.index, name='admin.hostel.room'),
    path('hostel/rooms/<int:h_id>/add', room.add, name='admin.hostel.room_add'),
    path('hostel/rooms/<int:h_id>/edit/<int:r_id>', room.edit, name='admin.hostel.room_edit'),
    path('hostel/rooms/<int:h_id>/delete/<int:r_id>', room.edit, name='admin.hostel.room_delete'),
    path('hostel/rooms/<int:h_id>/assign/<int:r_id>', room.assign, name='admin.hostel.room_assign'),
    path('hostel/rooms/<int:h_id>/un_assign/<int:r_id>', room.un_assign, name='admin.hostel.room_unassign'),

    path('hostel/change_request/approve/<int:id>', hostel.c_approve, name='admin.hostel.c_room'),
    path('hostel/change_request/reject/<int:id>', hostel.c_reject, name='admin.hostel.c_room.reject'),


    
    path('meal', meal.index, name='admin.meal'),
    path('meal/edit', meal.edit, name='admin.meal_edit'),
    
    path('notice', notice.index, name='admin.notice'),
    path('notice/add', notice.add, name='admin.notice_add'),
    path('notice/edit/<int:id>', notice.edit, name='admin.notice_edit'),
    
    path('billing', billing.index, name='admin.billing'),
    path('billing/add', billing.add, name='admin.billing_add'),
    path('billing/edit/<int:id>', billing.edit, name='admin.billing_edit'),
]