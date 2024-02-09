from django.shortcuts import render,redirect,reverse
from django.http import JsonResponse
from django.contrib import messages
from django_dump_die.middleware import dump
from ..models import Billing,User
from ..forms import BillingForm

prefix='admin/pages/'
def index(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        start=request.GET['start']
        perpage=request.GET['length']
        draw_val = request.GET['draw']
        search_text = request.GET['search[value]']
        query=Billing.objects.all().order_by('-date')
        if(search_text):
            query=query.filter(name__contains=search_text)
        total = query.count()
        datas=query[int(start):int(perpage)+int(start)].all()
        tmp=[]
        for i in datas:
            user=""
            user_address=""
            user_id=""
            if i.user:
                user=i.user.email
                user_address=i.user.address
                user_id=i.user.id
            tmp.append({
                'id':i.id,
                'date':i.date,
                'amount':i.amount,
                'remark':i.remark,
                'user':user,
                'user_address':user_address,
                'user_id':user_id
            })
        total = query.count()
        get_json_data = {"draw": int(draw_val), "recordsTotal":total,"recordsFiltered":total,"data":list(tmp)}
        return JsonResponse(get_json_data)
    
    return render(request,prefix+'billing/index.html')

def add(request):
    if request.method=='POST':
        form = BillingForm(request.POST)
        if form.is_valid():
            form.save(commit=True)
            messages.info(request,"Billing Added")
            return redirect(reverse('admin.billing'))
        else:
            dump(form)
            errors=form.errors.as_data()
            context = {  
                'errors':list(errors.values())
            } 
            return render(request,prefix+'billing/add.html',context) 
    
    students=User.objects.filter(role=2).values('id','email')
    return render(request,prefix+'billing/add.html',{'students':students})

def edit(request,id):
    data=Billing.objects.get(pk=id)
    if not data:
        messages.error(request,"Billing Not found")
        return redirect(reverse('admin.billing'))

    if request.method=='POST':
        date = request.POST['date']
        billing = request.POST['billing']
        if date : data.date = date
        if billing : data.billing = billing
        data.save()
        messages.info(request,"Billing Updated")
        return redirect(reverse('admin.billing'))
    
    return render(request,prefix+'billing/edit.html',{'data':data})