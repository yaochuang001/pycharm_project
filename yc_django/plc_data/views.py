from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
# Create your views here.
def index(request, month):
    value = 'this is test'
    print(value)
    context = {'key': 'hello','password':'199128'}
    #return render(request, 'dis_zs_dg/index.html', context=context)
    return JsonResponse(context, safe=False)