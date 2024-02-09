from django.shortcuts import render,redirect,reverse
from django.http import JsonResponse
from django.contrib import messages
from django_dump_die.middleware import dump
from admin.models import Meal
from datetime import datetime
from datetime import date
prefix='student/pages/'
def index(request):

    dt = datetime.now()
    day=dt.strftime('%A')

    datas=Meal.objects.get(day=day)
    title=str(date.today())+','+day
    return render(request,prefix+'meal/index.html', {'meals':datas,'title':title})