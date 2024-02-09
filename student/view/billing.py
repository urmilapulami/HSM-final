from django.shortcuts import render,redirect,reverse
from django.http import JsonResponse
from django.contrib import messages
from django_dump_die.middleware import dump
from admin.models import Billing

prefix='student/pages/'
def index(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        start=request.GET['start']
        perpage=request.GET['length']
        draw_val = request.GET['draw']
        search_text = request.GET['search[value]']
        user=request.user
        query=Billing.objects.filter(user_id=user.id).all().order_by('-date')
        if(search_text):
            query=query.filter(name__contains=search_text)
        total = query.count()
        datas=query[int(start):int(perpage)+int(start)].all()
        tmp=[]
        for i in datas:
            user=""
            user_address=""
            if i.user:
                user=i.user.email
                user_address=i.user.address
            tmp.append({
                'id':i.id,
                'date':i.date,
                'amount':i.amount,
                'remark':i.remark,
                'user':user,
                'user_address':user_address
            })
        total = query.count()
        get_json_data = {"draw": int(draw_val), "recordsTotal":total,"recordsFiltered":total,"data":list(tmp)}
        return JsonResponse(get_json_data)
    
    return render(request,prefix+'billing/index.html')
    