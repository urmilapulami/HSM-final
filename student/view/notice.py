from django.shortcuts import render,redirect,reverse
from django.http import JsonResponse
from admin.models import Notice
from django.db.models import Q

prefix='student/pages/'
def index(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        start=request.GET['start']
        perpage=request.GET['length']
        draw_val = request.GET['draw']
        search_text = request.GET['search[value]']
        user=request.user
        query=Notice.objects.all().filter(Q(user=user.id) | Q(user__isnull=True)).order_by('-date')
        if(search_text):
            query=query.filter(name__contains=search_text)
        total = query.count()
        datas=query[int(start):int(perpage)+int(start)].values()
        total = query.count()
        get_json_data = {"draw": int(draw_val), "recordsTotal":total,"recordsFiltered":total,"data":list(datas)}
        return JsonResponse(get_json_data)