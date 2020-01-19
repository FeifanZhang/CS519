from shoppingCart import views
from django.urls import include, path
from shoppingCart import cartViews
from shoppingCart import orderViews
from shoppingCart import promotionViews
"""
the url path distribution
"""
urlpatterns = [
    path('signIn/',views.signIn,name="signIn"),
    path('register/',views.register,name="register"),
    path('homepage/',views.homepage,name="homepage"),
    path('logOut/',views.logOut,name="logOut"),
    path('cartPage/',cartViews.cartPage,name="cartPage"),
    path('addIntoCart/',cartViews.addIntoCart,name="addIntoCart"),
    path('modifyQuantity/',cartViews.modifyQuantity,name="modifyQuantity"),
    path('deleteProductItem/',cartViews.deleteCartItem,name='deleteProductItem'),
    path('checkOut/',cartViews.checkOut,name='checkOut'),
    path('orderPage/',orderViews.orderPage, name="orderPage"),
    path('promotionPage/',promotionViews.promotionPage, name="promotionPage"),
]