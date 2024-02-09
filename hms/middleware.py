from django.shortcuts import render,redirect,reverse

from django_dump_die.middleware import dump
class adminMiddleware:
    ADMIN=1
    STUDENT=2
    EMPLOYEE=3
    WHITELISTED_URLS = [
        "/admin/login",
        "/student/login",
        "/employee/login",
    ]
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user=request.user
        response = self.get_response(request)
        if request.path.startswith("/admin"):
            if request.path in self.WHITELISTED_URLS:
                if user.is_authenticated:
                    return redirect(reverse('admin.dashboard'))
                else:
                    return response
            if not user.is_authenticated:
                return redirect(reverse('admin.login'))
            else:
                if user.role==self.ADMIN:
                    return response
                else:
                    return render(request,'un_authorized.html', {})
        
        if request.path.startswith("/student"):
            if request.path in self.WHITELISTED_URLS:
                if user.is_authenticated:
                    return redirect(reverse('student.dashboard'))
                else:
                    return response
            if not user.is_authenticated:
                return redirect(reverse('student.login'))
            else:
                if user.role==self.STUDENT:
                    return response
                else:
                    return render(request,'un_authorized.html', {})
        
        if request.path.startswith("/employee"):
            if request.path in self.WHITELISTED_URLS:
                if user.is_authenticated:
                    return redirect(reverse('employee.dashboard'))
                else:
                    return response
            if not user.is_authenticated:
                return redirect(reverse('employee.login'))
            else:
                if user.role==self.EMPLOYEE:
                    return response
                else:
                    return render(request,'un_authorized.html', {})
        
        return response
