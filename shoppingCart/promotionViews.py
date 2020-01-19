from django.shortcuts import render
from django.shortcuts import redirect
from shoppingCart.models import *
import  datetime
import json
from django.http import HttpResponse
import  simplejson
from django.contrib import auth
from wsgiref.simple_server import make_server

user=User
promotionList=[]

"""
display which promotionCode can be use
:param request: HTTP request
:returns: HTTP response
:raises keyErrors: No promotion in database or no promotion can be used
"""
def promotionPage(request):
    global user
    user.username = request.COOKIES.get('username')
    user = User.objects.filter(username=user.username)[0]
    global promotionList
    promotionList = []
    if (Promotion.objects.all().exists()):
        for i in Promotion.objects.all():
            today = datetime.date.today()
            start = datetime.datetime.strftime(i.startDate, '%Y-%m-%d')
            expire = datetime.datetime.strftime(i.expireDate, '%Y-%m-%d')
            today = datetime.datetime.strftime(today, '%Y-%m-%d')
            if (expire > today and start <= today):
                element={'productName':Products.objects.filter(id=i.productID_id)[0].name,'discount':str(i.discount)+'% Off','promotionNum':i.promotionNum,'expireDate':i.expireDate}
                promotionList.append(element)
        request = render(request, 'promotionPage.html',{'promotionList': promotionList, 'username': user.username})
    else:
        request = render(request, 'promotionPage.html',{'promotionList': promotionList,'username': user.username})
    request.set_cookie('username', user.username)
    promotionList = []
    return request