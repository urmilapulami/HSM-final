from django.shortcuts import render,redirect,reverse
from django.http import JsonResponse
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login,logout,authenticate
from django.contrib import messages
from django_dump_die.middleware import dump
from .models import User,Hostel,Room,Billing
from .forms import UserForm
from django.core import serializers
from django.forms.models import model_to_dict
from django.db.models.functions import ExtractMonth
from django.db.models import Sum,Count

prefix='admin/pages/'
def u_login(request):
    # raise Exception(reverse('admin.dashboard'))
    if request.method=='POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.role==1:
                    login(request, user)
                    messages.info(request, f"You are now logged in as {username}.")
                    return redirect(reverse('admin.dashboard'))
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
    return redirect(reverse('admin.login'))

def dashboard(request):
    # dump(request.user)
    hostels=Hostel.objects.all()
    capacity_l=[]
    capacity_c=[]
    capacity_o=[]
    month=['Jan','Feb','Mar','Apr','May','June','July','Aug','Sept','Oct','Nov','Dec']
    for hostel in hostels:
        query=Room.objects.filter(hostel=hostel.id)
        c=query.count()
        o=query.filter(user_id__isnull=False).count()
        capacity_l.append(hostel.name)
        capacity_c.append(c)
        capacity_o.append(o)
    billing_l=[]
    billing_i=[]
    month=['Jan','Feb','Mar','Apr','May','June','July','Aug','Sept','Oct','Nov','Dec']
    billings=Billing.objects.annotate(month=ExtractMonth('date')).values('month').annotate(count=Sum('amount')) .values('month', 'count').order_by('month')
    for billing in billings:
        billing_l.append(month[billing['month']-1])
        billing_i.append(billing['count'])
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        datas = {
             "capacity":{
                "label":capacity_l,
                "capacity":capacity_c,
                "occupied":capacity_o,
            },
            "income":{
                "label":billing_l,
                "income":billing_i,
            },
            "attendence":{
                "label":[
                    '01/01',
                    '01/02',
                    '01/03',
                    '01/04',
                    '01/05',
                    '01/06',
                    '01/07',
                    '01/08',
                    '01/09',
                    '01/10',
                    '01/11',
                    '01/12',
                    '01/13',
                    '01/14',
                    '01/15',
                    '01/16',
                    '01/17',
                    '01/18',
                    '01/19',
                    '01/20',
                    '01/21',
                    '01/22',
                    '01/23',
                    '01/24',
                    '01/25',
                    '01/26',
                    '01/27',
                    '01/28',
                    '01/29',
                    '01/30',
                    ],
                "present":[
                    459,
                    234,
                    634,
                    543,
                    459,
                    423,
                    459,
                    344,
                    545,
                    423,
                    459,
                    459,
                    345,
                    123,
                    683,
                    765,
                    534,
                    459,
                    234,
                    459,
                    809,
                    459,
                    342,
                    423,
                    459,
                    767,
                    459,
                    345,
                    346,
                    234,
                ],
            }
        }
        return JsonResponse(datas, safe=False)

    return render(request,prefix+'dashboard.html', {})

def profile(request):
    return render(request,prefix+'profile.html', {})

def student(request):
    # users=User.objects.filter(role=2).values()
    # dump(list(users))
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        # users=User.objects.filter(role=2)
        start=request.GET['start']
        perpage=request.GET['length']
        draw_val = request.GET['draw']
        search_text = request.GET['search[value]']
        query=User.objects.filter(role=2)
        if(search_text):
            query=query.filter(username__contains=search_text)
            # query.filter(username__icontains=search_text)
        total = query.count()
        users=query[int(start):int(perpage)+int(start)].values()
        total = query.count()        # dump(users)
        get_json_data = {"draw": int(draw_val), "recordsTotal":total,"recordsFiltered":total,"data":list(users)}
        return JsonResponse(get_json_data)
    return render(request,prefix+'students/student.html', {})

def student_add(request):
    if request.method=='POST':
        form = UserForm(request.POST,request.FILES)
        if form.is_valid():
            # handle_uploaded_file(request.FILES["file"])
            username = request.POST['username']
            password = request.POST['password1']
            email = request.POST['email']
            gender = request.POST['gender']
            mobile_number = request.POST['mobile_number']
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            address = request.POST['address']
            user=User.objects.create_student(username,email,password)
            user.gender = gender
            user.mobile_number = mobile_number
            user.first_name = first_name
            user.last_name = last_name
            user.address = address
            user.image = request.FILES["image"]
            user.save()
            messages.info(request,"Student Added")
            return redirect(reverse('admin.student'))
        else:
            post_data = {k:v[0] for k,v in dict(request.POST).items()}
            errors=form.errors.as_data()
            post_data['errors']=list(errors.values())
            return render(request,prefix+'students/addStudent.html',post_data) 
    return render(request,prefix+'students/addStudent.html',{})
def student_edit(request,id):
    user=User.objects.get(pk=id)
    if not user:
        messages.error(request,"Student Not found")
        return redirect(reverse('admin.student'))

    if request.method=='POST':
        email = request.POST['email']
        gender = request.POST['gender']
        mobile_number = request.POST['mobile_number']
        address = request.POST['address']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        if email : user.email = email
        if first_name : user.first_name = first_name
        if last_name : user.last_name = last_name
        if gender : user.gender = gender
        if mobile_number : user.mobile_number = mobile_number
        if address : user.address = address
        user.save()
        messages.info(request,"Student Updated")
        return redirect(reverse('admin.student'))
    
    return render(request,prefix+'students/editStudent.html',{'data':user})
def student_view(request,id):
    user=User.objects.get(pk=id)
    if not user:
        messages.error(request,"Student Not found")
        return redirect(reverse('admin.student'))
    room=[]
    billings=[]
    try:
        room=Room.objects.get(user_id=id)
        billings=Billing.objects.filter(user_id=id).order_by('-date').all()
    except Exception as ez:
        pass
        

    return render(request,prefix+'students/viewStudent.html',{'data':user,'room':room,'billings':billings})
def student_activete(request,id):
    user=User.objects.get(pk=id)
    user.is_active=1
    user.save()
    return JsonResponse({'message':'Student Activeted'})

def student_deactivete(request,id):
    user=User.objects.get(pk=id)
    user.is_active=False
    user.save()
    return JsonResponse({'message':'Student DeActiveted'})



def employee(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        start=request.GET['start']
        perpage=request.GET['length']
        draw_val = request.GET['draw']
        search_text = request.GET['search[value]']
        query=User.objects.filter(role=3)
        if(search_text):
            query=query.filter(username__contains=search_text)
        total = query.count()
        users=query[int(start):int(perpage)+int(start)].values()
        total = query.count()        # dump(users)
        get_json_data = {"draw": int(draw_val), "recordsTotal":total,"recordsFiltered":total,"data":list(users)}
        return JsonResponse(get_json_data)
    return render(request,prefix+'employee/employee.html', {})

def employee_add(request):
    if request.method=='POST':
        form = UserForm(request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password1']
            email = request.POST['email']
            gender = request.POST['gender']
            mobile_number = request.POST['mobile_number']
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            address = request.POST['address']
            user=User.objects.create_employee(username,email,password)
            user.gender = gender
            user.mobile_number = mobile_number
            user.first_name = first_name
            user.last_name = last_name
            user.address = address
            user.save()
            messages.info(request,"employee Added")
            return redirect(reverse('admin.employee'))
        else:
            errors=form.errors.as_data()
            context = {  
                'errors':list(errors.values())
            } 
            return render(request,prefix+'employee/addEmployee.html',context) 
    return render(request,prefix+'employee/addEmployee.html',{})

def employee_edit(request,id):
    user=User.objects.get(pk=id)
    if not user:
        messages.error(request,"employee Not found")
        return redirect(reverse('admin.employee'))

    if request.method=='POST':
        email = request.POST['email']
        gender = request.POST['gender']
        mobile_number = request.POST['mobile_number']
        address = request.POST['address']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        if email : user.email = email
        if first_name : user.first_name = first_name
        if last_name : user.last_name = last_name
        if gender : user.gender = gender
        if mobile_number : user.mobile_number = mobile_number
        if address : user.address = address
        user.save()
        messages.info(request,"employee Updated")
        return redirect(reverse('admin.employee'))
    
    return render(request,prefix+'employee/editEmployee.html',{'data':user})
def employee_activete(request,id):
    user=User.objects.get(pk=id)
    user.is_active=1
    user.save()
    return JsonResponse({'message':'employee Activeted'})

def employee_deactivete(request,id):
    user=User.objects.get(pk=id)
    user.is_active=False
    user.save()
    return JsonResponse({'message':'employee DeActiveted'})


def admin(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        start=request.GET['start']
        perpage=request.GET['length']
        draw_val = request.GET['draw']
        search_text = request.GET['search[value]']
        query=User.objects.filter(role=1)
        if(search_text):
            query=query.filter(username__contains=search_text)
        total = query.count()
        users=query[int(start):int(perpage)+int(start)].values()
        total = query.count()        # dump(users)
        get_json_data = {"draw": int(draw_val), "recordsTotal":total,"recordsFiltered":total,"data":list(users)}
        return JsonResponse(get_json_data)
    return render(request,prefix+'admin/Admin.html', {})

def admin_add(request):
    if request.method=='POST':
        form = UserForm(request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password1']
            email = request.POST['email']
            gender = request.POST['gender']
            mobile_number = request.POST['mobile_number']
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            address = request.POST['address']
            user=User.objects.create_superuser(username,email,password)
            user.gender = gender
            user.mobile_number = mobile_number
            user.first_name = first_name
            user.last_name = last_name
            user.address = address
            user.save()
            messages.info(request,"admin Added")
            return redirect(reverse('admin.admin'))
        else:
            post_data = {k:v[0] for k,v in dict(request.POST).items()}
            errors=form.errors.as_data()
            post_data['errors']=list(errors.values())
            return render(request,prefix+'admin/addAdmin.html',post_data) 
    return render(request,prefix+'admin/addAdmin.html',{})

def admin_edit(request,id):
    user=User.objects.get(pk=id)
    if not user:
        messages.error(request,"admin Not found")
        return redirect(reverse('admin.admin'))

    if request.method=='POST':
        email = request.POST['email']
        gender = request.POST['gender']
        mobile_number = request.POST['mobile_number']
        address = request.POST['address']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        if email : user.email = email
        if first_name : user.first_name = first_name
        if last_name : user.last_name = last_name
        if gender : user.gender = gender
        if mobile_number : user.mobile_number = mobile_number
        if address : user.address = address
        user.save()
        messages.info(request,"admin Updated")
        return redirect(reverse('admin.admin'))
    
    return render(request,prefix+'admin/editAdmin.html',{'data':user})
def admin_activete(request,id):
    user=User.objects.get(pk=id)
    user.is_active=1
    user.save()
    return JsonResponse({'message':'admin Activeted'})

def admin_deactivete(request,id):
    user=User.objects.get(pk=id)
    user.is_active=False
    user.save()
    return JsonResponse({'message':'admin DeActiveted'})

def billing(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        get_json_data = {"draw": 1, "recordsTotal":0,"recordsFiltered":0,"data":[]}
        return JsonResponse(get_json_data);
    return render(request,prefix+'billing/billing.html', {})

def billing_add(request):
    return render(request,prefix+'billing/addbilling.html', {})


