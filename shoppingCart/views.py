from django.shortcuts import render
from django.shortcuts import redirect
from shoppingCart.models import *
import json
from django.http import HttpResponse
import  simplejson
from django.contrib import auth
from wsgiref.simple_server import make_server


# Create your views here.

user=User
productList=[]
carouselList=[]

"""
to display homepage
:param request: HTTP request
:returns: HTTP response with tow cookies: isSuperuser and username
:raises keyErrors: None 
"""
def homepage(request):
    global user
    global productList
    productList=[]
    if(request.POST.get('keyword')==None or request.POST.get('keyword')==''or request.POST.get('keyword')=='None'):
        if(Products.objects.all().exists()):
            for i in Products.objects.all():
                element = {'id': i.id, 'name': i.name, 'quantity': i.quantity, 'introduction': i.introduction,
                'img':'../../../'+ i.img.url,'price':i.price}
                productList.append(element)
    else:
        for i in Products.objects.filter(name__contains=str(request.POST.get('keyword'))):
            element={'id': i.id, 'name': i.name, 'quantity': i.quantity, 'introduction': i.introduction,
                     'img': '../../../' + i.img.url,'price':i.price}
            productList.append(element)
    if (request.COOKIES.get('username') == None or request.COOKIES.get('username')==''):
        return render(request, 'main.html',globals())
    elif(User.objects.filter(username=request.COOKIES.get('username')).exists()):
        user=User.objects.filter(username=request.COOKIES.get('username'))[0]
        request = render(request,'main.html',{'username': user.username, 'is_superuser': user.is_superuser,'productList':productList})
        request.set_cookie('username', user.username)
        request.set_cookie('is_superuser',user.is_superuser)
    else:
        return render(request, 'main.html',{'productList':productList})
    return  request

"""
let the user sign in
:param request: HTTP request
:returns: HTTP response with tow cookies: isSuperuser and username
:raises keyErrors: email is invalid, password is invalid, username is invalid 
"""
def signIn(request):
    request = simplejson.loads(request.body)
    email = request['email']
    password = request['password']
    # empty or lack data in request
    if (email == None):
        error = {'error': 'email is empty'}
        request = HttpResponse(json.dumps(error))
       # request['error'] = 'email is empty'
    elif (password == None):
        error = {'error': 'password is empty'}
        request = HttpResponse((json.dumps(error)))
    elif (len(password) < 5):
        error = {'error': 'length of password cannot be less than 5'}
        request = HttpResponse(json.dumps(error))
    elif (User.objects.filter(email=email).exists()):
        user=User.objects.filter(email=email)[0]
        if(user.check_password(password)==False):
            error = {'error': 'password is wrong'}
            request = HttpResponse((json.dumps(error)))
        elif(user.is_active):
            request = HttpResponse()
            request.set_cookie('is_superuser', user.is_superuser)
            request.set_cookie('username', user.username)
        else:
            error = {'error': 'the account is not allow to use'}
            request = HttpResponse(json.dumps(error))
    else:
        request = HttpResponse()
       # request['error'] = 'the account is not exist'
   # print(request.get('error'))

    return request

"""
let the user register
:param request: HTTP request
:returns: HTTP response with two cookies: isSuperuser and username
:raises keyErrors: email is invalid, password is invalid, username is invalid 
"""
def register(request):
    request = simplejson.loads(request.body)
    email = request['email']
    password = request['password']
    username = request['username']

    if (email == None):
        error = {'error': 'email is empty'}
        request = HttpResponse((json.dumps(error)))
    elif (password == None):
        error = {'error': 'password is empty'}
        request = HttpResponse((json.dumps(error)))
    elif (username == None):
        error = {'error': 'username is empty'}
        request = HttpResponse((json.dumps(error)))
    # emial and password are assigned
    elif (User.objects.filter(email=email).exists() or User.objects.filter(
            password=password).exists() or User.objects.filter(username=username).exists()):
        request = HttpResponse(json.dumps({"error": "the account info had been exists"}))
    elif (len(username) <= 4):
        request = HttpResponse(json.dumps({"error": "length of username must be more than 4"}))
    elif (len(password) < 6):
        request = HttpResponse(json.dumps({"error": "length of password must be more than 6"}))
    else:
        user = User.objects.create_user(username=username, password=password,email=email,searchingRecord='None',is_active=True, is_superuser=False)
        user.save()
        print('success for confirm register')
        request = HttpResponse()
        request.set_cookie('is_superuser',user.is_superuser)
        request.set_cookie('username',user.username)
    return request

"""
let the user log out
:param request: HTTP request
:returns: HTTP response
:raises keyErrors: None 
"""
def logOut(request):
    request=redirect('/shoppingCart/homepage/')
    request.delete_cookie('is_superuser')
    request.delete_cookie('username')
    return request




