from django.shortcuts import render,redirect,reverse
from django.http import JsonResponse
from django.contrib import messages
from django_dump_die.middleware import dump
from ..models import Notice
from ..forms import NoticeForm

prefix='admin/pages/'
def index(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        start=request.GET['start']
        perpage=request.GET['length']
        draw_val = request.GET['draw']
        search_text = request.GET['search[value]']
        query=Notice.objects.all().filter(user__isnull=True).order_by('-date')
        if(search_text):
            query=query.filter(name__contains=search_text)
        total = query.count()
        datas=query[int(start):int(perpage)+int(start)].values()
        total = query.count()
        get_json_data = {"draw": int(draw_val), "recordsTotal":total,"recordsFiltered":total,"data":list(datas)}
        return JsonResponse(get_json_data)
    
    return render(request,prefix+'notice/index.html')

def add(request):
    if request.method=='POST':
        form = NoticeForm(request.POST)
        if form.is_valid():
            form.save(commit=True)
            messages.info(request,"Notice Added")
            return redirect(reverse('admin.notice'))
        else:
            errors=form.errors.as_data()
            context = {  
                'errors':list(errors.values())
            } 
            return render(request,prefix+'notice/add.html',context) 
    return render(request,prefix+'notice/add.html',{})

def edit(request,id):
    data=Notice.objects.get(pk=id)
    if not data:
        messages.error(request,"Notice Not found")
        return redirect(reverse('admin.notice'))

    if request.method=='POST':
        date = request.POST['date']
        notice = request.POST['notice']
        if date : data.date = date
        if notice : data.notice = notice
        data.save()
        messages.info(request,"Notice Updated")
        return redirect(reverse('admin.notice'))
    
    return render(request,prefix+'notice/edit.html',{'data':data})