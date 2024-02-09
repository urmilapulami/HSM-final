from django.shortcuts import render,redirect,reverse
from django.http import JsonResponse
from django.contrib import messages
from django_dump_die.middleware import dump
from ..models import Hostel,RoomChange,Room
from ..forms import HostelForm,NoticeForm
from datetime import date

prefix='admin/pages/'
def index(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        start=request.GET['start']
        perpage=request.GET['length']
        draw_val = request.GET['draw']
        search_text = request.GET['search[value]']
        query=Hostel.objects.all()
        if(search_text):
            query=query.filter(name__contains=search_text)
        total = query.count()
        datas=query[int(start):int(perpage)+int(start)].values()
        total = query.count()
        get_json_data = {"draw": int(draw_val), "recordsTotal":total,"recordsFiltered":total,"data":list(datas)}
        return JsonResponse(get_json_data)
    
    c_rooms=RoomChange.objects.all()
    return render(request,prefix+'hostel/index.html', {'c_rooms':c_rooms})


def c_approve(request,id):
    data=RoomChange.objects.get(pk=id)
    
    room=Room.objects.get(user_id=data.user_id)
    
    room.user_id = None
    room.save()

    room2=Room.objects.get(pk=data.room_id)
    
    room2.user_id = data.user_id
    room2.save()
    form = NoticeForm({'user':data.user_id,'date':date.today(),'notice':'Room Change Approved'})
    if form.is_valid():
        form.save(commit=True)
    RoomChange.objects.filter(id=id).delete()
    messages.info(request,"Request Approved")
    return redirect(reverse('admin.hostel'))

def c_reject(request,id):
    data=RoomChange.objects.get(pk=id)
    RoomChange.objects.filter(id=id).delete()
    form = NoticeForm({'user':data.user_id,'date':date.today(),'notice':'Room Change Rejected'})
    if form.is_valid():
        form.save(commit=True)
    messages.info(request,"Request Rejected")
    return redirect(reverse('admin.hostel'))
    

def add(request):
    if request.method=='POST':
        form = HostelForm(request.POST)
        if form.is_valid():
            form.save(commit=True)
            messages.info(request,"Hostel Added")
            return redirect(reverse('admin.hostel'))
        else:
            errors=form.errors.as_data()
            context = {  
                'errors':list(errors.values())
            } 
            return render(request,prefix+'hostel/add.html',context) 
    return render(request,prefix+'hostel/add.html',{})

def edit(request,id):
    data=Hostel.objects.get(pk=id)
    if not data:
        messages.error(request,"Hostel Not found")
        return redirect(reverse('admin.hostel'))

    if request.method=='POST':
        name = request.POST['name']
        note = request.POST['note']
        check=Hostel.objects.filter(name=name).exclude(id=id)
        if(check):
            messages.error(request,"Hostel Name Already Taken")
            return redirect(reverse('admin.hostel_edit', kwargs={'id':id}))

        if name : data.name = name
        if note : data.note = note
        data.save()
        messages.info(request,"Hostel Updated")
        return redirect(reverse('admin.hostel'))
    
    return render(request,prefix+'hostel/edit.html',{'data':data})