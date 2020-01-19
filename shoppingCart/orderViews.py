from django.shortcuts import render
from django.shortcuts import redirect
from shoppingCart.models import *
import json
from django.http import HttpResponse
import  simplejson
from django.contrib import auth
from wsgiref.simple_server import make_server
orderList=[]
user=User


"""
display the order page
:param request: HTTP request
:returns: HTTP response with two cookies: isSuperuser and username
:raises keyErrors: username is invalid, user has no order.
"""
def orderPage(request):
    if(request.COOKIES.get('username')==None):
        request=render('shoppingCart/homepage/')
    elif(User.objects.filter(username=request.COOKIES.get('username')).exists()):
        global user
        user=User.objects.filter(username=request.COOKIES.get('username'))[0]
        global orderList
        orderList = []
        if(Orders.objects.filter(userID_id=user.id).exists()):
            for i in Orders.objects.filter(userID_id=user.id):
                element={'productName':i.productName,'quantity':i.quantity, 'price':i.price,'addressee':i.addressee,'address':i.address}
                orderList.append(element)
    request=render(request,'order.html',{'orderList':orderList})
    request.set_cookie('username',user.username)
    return request


