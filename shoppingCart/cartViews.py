from django.shortcuts import render
from django.shortcuts import redirect
from shoppingCart.models import *
from decimal import Decimal
import  datetime
import json
from django.http import HttpResponse
import  simplejson
from django.contrib import auth
from wsgiref.simple_server import make_server

user=User
cartList=[]
taxList={'WA':0.0892,'CA':0.0825,'NV':0.0798,'ID':0.0630,'UT':0.0676,'AZ':0.0825,'NM':0.0750,
         'CO':0.0750,'WY':0.0540,'ND':0.0678,'SD':0.0639,'NE':0.0689,'KS':0.0620,'OK':0.0886,
         'MN':0.0730,'IA':0.0680,'MO':0.0789,'AR':0.0930,'LA':0.0998,'WI':0.0542,'IL':0.0864,
         'KY':0.0600,'MS':0.0702,'AL':0.0901,'TN':0.0946,'IN':0.0700,'MI':0.0600,'OH':0.0714,
         'WV':0.0629,'VA':0.0563,'PA':0.0634,'NY':0.0849,'ME':0.0550,'NC':0.0690,'SC':0.0722,
         'GA':0.0700,'FL':0.0680}

"""
checking if the promotion is valid or not
:param Int: promotionNum
       Int: productId
:returns: int(discount), if return -1:the promotion code is invalid, return -2: there is not promotion code in here.
:raises keyErrors: None 
"""
def checkPromoton(promotionNum,productId):
    if(Promotion.objects.filter(promotionNum=promotionNum,productID_id=productId).exists()):
        promotion=Promotion.objects.filter(promotionNum=promotionNum,productID_id=productId)[0]
        today = datetime.date.today()
        start=datetime.datetime.strftime(promotion.startDate,'%Y-%m-%d')
        expire=datetime.datetime.strftime(promotion.expireDate,'%Y-%m-%d')
        today=datetime.datetime.strftime(today,'%Y-%m-%d')
        if (expire>today and start<=today):
            print(promotion.discount)
            return  promotion.discount
        else:
            return -1
    else:
        return -2
"""
check out
:param request: HTTP request
:returns: HTTP response with two cookies: isSuperuser and username
:raises keyErrors: username is invalid, the item that user want to check which is not exsist,the quantity is 0,
"""
def checkOut(request):
    global user
    user.username = request.COOKIES.get('username')
    cartIdList=request.POST.getlist('check_items_id')
    if(cartIdList==None or cartIdList=='' or len(cartIdList)==0):
        request=redirect('/shoppingCart/cartPage/')
    else:
        for i in cartIdList:
            order=Orders
            cart=Cart.objects.filter(id=i)[0]
            product=Products.objects.filter(id=cart.productID_id)[0]
            order.productName=product.name
            if(request.POST.get('promotionNum')==None or request.POST.get('promotionNum')=='' or request.POST.get('promotionNum')=='None'):
                discount=0
            else:
                discount=checkPromoton(request.POST.get('promotionNum'),product.id)
            if(discount==-1):
                request=redirect('/shoppingCart/cartPage/')
                request.set_cookie('username',user.username)
                return request
            elif (discount==-2):
                request=redirect('/shoppingCart/cartPage/')
                request.set_cookie('username', user.username)
                return request
            order.price=float(request.POST.get('price'))*float(100-discount)/100
            order.quantity=Cart.objects.filter(id=i)[0].quantity
            order.productID=product.id
            order.userID=Cart.objects.filter(id=i)[0].userID
            order.address=request.POST.get('address')
            order.addressee=request.POST.get('firstName')+request.POST.get('lastName')
            string=str(request.POST.get('firstName'))+str(request.POST.get('lastName'))
            newOrder=Orders.objects.create(productName=product.name,
                                           quantity=Cart.objects.filter(id=i)[0].quantity,
                                          userID_id=Cart.objects.filter(id=i)[0].userID_id,
                                           address=request.POST.get('address'),
                                           addressee=string,
                                           price=order.price)
            newOrder.save()
            Cart.objects.filter(id=i).delete()
        request=redirect('/shoppingCart/cartPage/')
    request.set_cookie('username',user.username)
    return request

"""
display the items in cart
:param request: HTTP request
:returns: HTTP response with two cookies: isSuperuser and username
:raises keyErrors: username is invalid, the item that user want to display which is not exsist
"""
def cartPage(request):
    global user
    user.username = request.COOKIES.get('username')
    user = User.objects.filter(username=user.username)[0]
    global cartList
    cartList=[]
    if(Cart.objects.filter(userID_id=user.id).exists()):
        for i in Cart.objects.filter(userID_id=user.id):
            element={'price':Products.objects.filter(id=i.productID_id)[0].price,'userId':i.userID,'productId':i.productID,
            'id':i.id,'quantity':i.quantity,'productName':i.productName}
            cartList.append(element)
        global taxList
        request=render(request, 'cart.html', {'cartList':cartList,'username':user.username,'is_superuser':user.is_superuser,'taxList':taxList})
    else:
        request=render(request, 'cart.html', {'cartList':cartList,'username':user.username,'is_superuser':user.is_superuser,'taxList':taxList})
    request.set_cookie('username', user.username)
    cartList=[]
    return request

"""
add the item in cart
:param request: HTTP request
:returns: HTTP response with two cookies: isSuperuser and username
:raises keyErrors: username is invalid, the item that user want to add which is not exsist,the quantity in invalid
"""
def addIntoCart(request):
    global user
    user.username=request.COOKIES.get('username')
    if( User.objects.filter(username=user.username).count()==0):
        request = redirect('/shoppingCart/homepage/')
        return request
    user = User.objects.filter(username=user.username)[0]
    product=Products.objects.filter(id=request.POST.get('productId'))[0]
    if (product.quantity <= 0):
        request = redirect('/shoppingCart/homepage/')
    elif(Cart.objects.filter(productID_id=product.id,userID_id=user.id).exists()):
        Products.objects.filter(id=request.POST.get('productId')).update(quantity=product.quantity - 1)
        newCartItem=Cart.objects.filter(productID_id=product.id,userID_id=user.id)[0]
        Cart.objects.filter(id=newCartItem.id).update(quantity=newCartItem.quantity+1)
        request = redirect('/shoppingCart/homepage/')
    else:
        Products.objects.filter(id=request.POST.get('productId')).update(quantity=product.quantity-1)
        user=User.objects.filter(username=user.username)[0]
        newCartItem=Cart.objects.create(productID_id=product.id,productName=product.name,quantity=1,userID_id=user.id)
        newCartItem.save()
        request=redirect('/shoppingCart/homepage/')
    request.set_cookie(user.username)
    return request

"""
delete the item in cart
:param request: HTTP request
:returns: HTTP response with two cookies: isSuperuser and username
:raises keyErrors: username is invalid, the item that user want to delete which is not exsist
"""
def modifyQuantity(request):
    global user
    user.username = request.COOKIES.get('username')
    user = User.objects.filter(username=user.username)[0]
    quantity=int(request.POST.get('quantity'))
    cart = Cart.objects.filter(id=request.POST.get('cartId'))[0]
    product=Products.objects.filter(id=cart.productID_id)[0]
    if(product.quantity<quantity):
        request = redirect('/shoppingCart/cartPage/')
    else:
        Products.objects.filter(id=product.id).update(quantity=product.quantity-quantity)
        Cart.objects.filter(id=cart.id).update(quantity=quantity)
        request = redirect('/shoppingCart/cartPage/')
    request.set_cookie('username',user.username)
    return request

"""
delete the item in cart
:param request: HTTP request
:returns: HTTP response with two cookies: isSuperuser and username
:raises keyErrors: username is invalid, the item that user wants to delete is not exsist
"""
def deleteCartItem(request):
    global user
    user.username = request.COOKIES.get('username')
    user = User.objects.filter(username=user.username)[0]
    cartIdList=str(request.POST.get('delete_items_id'))
    cartIdList=cartIdList.split(',')
    print(cartIdList)
    if(request.POST.get('delete_items_id')==None or request.POST.get('delete_items_id')==''):
        request = redirect('/shoppingCart/cartPage/')
    else:
        for i in cartIdList:
            Cart.objects.filter(id=int(i)).delete()
        request=redirect('/shoppingCart/cartPage/')
    request.set_cookie('username', user.username)
    return request