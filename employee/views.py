from django.shortcuts import render,redirect,reverse
from django.http import JsonResponse
from django.contrib.auth.forms import AuthenticationForm #add this
from django.contrib.auth import login,logout,authenticate #add this
from django.contrib import messages
from django_dump_die.middleware import dump

prefix='employee/pages/'
def u_login(request):
    
    if request.method=='POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.role==3:
                    login(request, user)
                    messages.info(request, f"You are now logged in as {username}.")
                    return redirect(reverse('employee.dashboard'))
                else:
                    messages.error(request,"Invalid username or password.")
            else:
                messages.error(request,"Invalid username or password.")
        else:
            messages.error(request,"Invalid username or password.")
    return render(request,prefix+'login.html',{})
def u_logout(request):
    logout(request)
    messages.info(request, f"Logout.")
    return redirect(reverse('employee.login'))
def dashboard(request):
    return render(request,prefix+'dashboard.html', {})

def profile(request):
    return render(request,prefix+'profile.html', {})

