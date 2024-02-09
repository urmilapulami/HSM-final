from django.shortcuts import render,redirect,reverse
from django.http import JsonResponse
from django.contrib import messages
from django_dump_die.middleware import dump
from ..models import Room,Hostel,User
from ..forms import RoomForm

prefix='admin/pages/'
def index(request,h_id):
    udatas=Room.objects.filter(user_id__isnull=False).values('user_id')
    udata=[]
    for i in udatas:
        udata.append(i['user_id'])
    hostel=Hostel.objects.get(pk=h_id)
    students=User.objects.filter(role=2).exclude(id__in=udata).values('id','email')
    if not hostel:
        messages.error(request,"Hostel Not found")
        return redirect(reverse('admin.hostel'))
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        start=request.GET['start']
        perpage=request.GET['length']
        draw_val = request.GET['draw']
        search_text = request.GET['search[value]']
        query=Room.objects.filter(hostel=h_id)
        if(search_text):
            query=query.filter(name__contains=search_text)
        total = query.count()
        datas=query[int(start):int(perpage)+int(start)].all()
        tmp=[]
        for i in datas:
            user="Not Assigned"
            user_address=""
            user_id=""
            if i.user:
                user=i.user.email
                user_id=i.user.id
                user_address=i.user.address
            tmp.append({
                'id':i.id,
                'name':i.name,
                'floor':i.floor,
                'note':i.note,
                'user':user,
                'user_address':user_address,
                'user_id':user_id
            })
        total = query.count()
        get_json_data = {"draw": int(draw_val), "recordsTotal":total,"recordsFiltered":total,"data":list(tmp)}
        return JsonResponse(get_json_data)
    return render(request,prefix+'room/index.html', {'hostel':hostel,'students':students})

def add(request,h_id):
    hostel=Hostel.objects.get(pk=h_id)
    if not hostel:
        messages.error(request,"Hostel Not found")
        return redirect(reverse('admin.hostel'))
    if request.method=='POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save(commit=True)
            messages.info(request,"Room Added")
            return redirect(reverse('admin.hostel.room', kwargs={'h_id':h_id}))
        else:
            errors=form.errors.as_data()
            context = {  
                'hostel':hostel,
                'errors':list(errors.values())
            } 
            return render(request,prefix+'room/add.html',context) 
    return render(request,prefix+'room/add.html',{'hostel':hostel})

def edit(request,h_id,r_id):
    hostel=Hostel.objects.get(pk=h_id)
    if not hostel:
        messages.error(request,"Hostel Not found")
        return redirect(reverse('admin.hostel'))
    data=Room.objects.get(pk=r_id)
    if not data:
        messages.error(request,"Room Not found")
        return redirect(reverse('admin.room'))

    if request.method=='POST':
        name = request.POST['name']
        note = request.POST['note']
        check=Room.objects.filter(name=name).exclude(id=r_id)
        if(check):
            messages.error(request,"Room Name Already Taken")
            return redirect(reverse('admin.hostel.room_edit', kwargs={'h_id':h_id,'r_id':r_id}))

        if name : data.name = name
        if note : data.note = note
        data.save()
        messages.info(request,"Room Updated")
        return redirect(reverse('admin.hostel.room',kwargs={'h_id':h_id}))
    
    return render(request,prefix+'room/edit.html',{'data':data,'hostel':hostel})

def assign(request,h_id,r_id):
    hostel=Hostel.objects.get(pk=h_id)
    if not hostel:
        messages.error(request,"Hostel Not found")
        return redirect(reverse('admin.hostel'))
    data=Room.objects.get(pk=r_id)
    if not data:
        messages.error(request,"Room Not found")
        return redirect(reverse('admin.hostel.room',kwargs={'h_id':h_id}))

    if request.method=='POST':
        student = request.POST['student']
        check=Room.objects.filter(user_id=student).exclude(id=r_id)
        if(check):
            messages.error(request,"Already Assign")
            return redirect(reverse('admin.hostel.room',kwargs={'h_id':h_id}))

        data.user_id = student
        data.save()
        messages.info(request,"Room Updated")
        return redirect(reverse('admin.hostel.room',kwargs={'h_id':h_id}))
    
    return render(request,prefix+'room/edit.html',{'data':data,'hostel':hostel})

def un_assign(request,h_id,r_id):
    room=Room.objects.get(id=r_id)
    room.user_id = None
    room.save()
    messages.info(request,"Room Updated")
    return redirect(reverse('admin.hostel.room',kwargs={'h_id':h_id}))