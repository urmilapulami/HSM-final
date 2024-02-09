from django.shortcuts import render,redirect,reverse
from django.http import JsonResponse
from django.contrib import messages
from django_dump_die.middleware import dump
from ..models import Meal

prefix='admin/pages/'
def index(request):
    datas=Meal.objects.values()
    return render(request,prefix+'meal/index.html', {'meals':datas})

def edit(request):
    pk = request.POST['pk']
    name = request.POST['name']
    value = request.POST['value']
    data=Meal.objects.get(pk=pk)
    if name == 'breakfast':
        data.breakfast = value
    
    elif name == "lunch":
        data.lunch = value
    
    elif name == "dinner":
        data.dinner = value
    data.save()
    return JsonResponse({'message':'Updated'})