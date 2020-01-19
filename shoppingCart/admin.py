from django.contrib import admin
from shoppingCart.models import *
# Register your models here.
"""
the attribute of user data would show in admin system
"""
class MyUser(admin.ModelAdmin):
    #the way to display the user data
    list_display = ("username","email","password","id","is_superuser","is_active")
    search_fields = ("username",)
    ordering = ("username",)

"""
the attribute of product data would show in admin system
"""
class MyProducts(admin.ModelAdmin):
    list_display = ("name","quantity","price","popularity","introduction","img","id")
    search_fields =("name",)
    ording=("name",)

"""
the attribute of cart data would show in admin system
"""
class MyCarts(admin.ModelAdmin):
    list_display = ("productName", "quantity", "productID", "userID_id","id")
    search_fields = ("productName",)
    ording = ("productName",)

class MyOrders(admin.ModelAdmin):
    list_display = ("productName", "quantity", "userID_id","address","addressee", "id")
    search_fields = ("productName",)
    ording = ("productName",)

"""
the attribute of promotion data would show in admin system
"""
class MyPromotions(admin.ModelAdmin):
    list_display = ("productID","discount","promotionNum","startDate","expireDate","id")
    search_fields = ("id",)
    ordering = ("id",)

"""
the attribute of address data would show in admin system
"""
class MyAddress(admin.ModelAdmin):
    list_display = ("userID","state","city","detailAddress","address")
    search_fields = ("address")
    ordering = ("address")
admin.site.register(User,MyUser)
admin.site.register(Products,MyProducts)
admin.site.register(Cart,MyCarts)
admin.site.register(Orders,MyOrders)
admin.site.register(Promotion,MyPromotions)