from django_dump_die.middleware import dump
from admin.models import Room,RoomChange
from admin.forms import ChangeRoomForm

from django.shortcuts import render,redirect,reverse
from django.contrib import messages


prefix='student/pages/'
def index(request):
    user=request.user
    data=[]
    c_data=[]
    rooms=Room.objects.filter(user_id__isnull=True)
    try:
        data=Room.objects.get(user_id=user.id)
        c_data=RoomChange.objects.get(user_id=user.id)
    except Exception as ez:
        pass
    return render(request,prefix+'room/index.html', {'room':data,'rooms':rooms,'c_data':c_data})

def change(request):
    form = ChangeRoomForm(request.POST)
    if form.is_valid():
        form.save(commit=True)
        messages.info(request,"Requested")
        return redirect(reverse('student.room'))
    else:
        messages.error(request,"Error")
        return redirect(reverse('student.room'))