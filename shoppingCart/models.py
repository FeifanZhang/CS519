from django.db import models
from django.contrib.auth.models import AbstractUser
import django.utils.timezone as timezone

# Create your models here.



class User(AbstractUser):

    searchingRecord=models.CharField(max_length=512)
    date_joined=models.DateTimeField("date_joined",auto_now_add=True)
    last_login = models.DateTimeField("last_login",auto_now=True)
    first_name = models.deletion
    last_name = models.deletion
    groups = models.deletion
    user_permissions = models.deletion
    class Meta(AbstractUser.Meta):
        permissions=(("add_logentry","Can add log entry"),
                     ("change_logentry","Can change log entry"),
                     ("delete_logentry","Can delete log entry"),
                     ("view_logentry","Can view log entry"),
                     ("add_group","Can add group"),
                     ("change_group","Can change group"),
                     ("delete_group","Can delete group"),
                     ("view_group","Can view group"),
                     ("add_permission	Can","add permission"),
                     ("change_permission","Can change permission"),
                     ("delete_permission","Can delete permission"),
                     ("view_permission","Can view permission"),
                     ("add_contenttype","Can add content type"),
                     ("change_contenttype","Can change content type"),
                     ("delete_contenttype","Can delete content type"),
                     ("view_contenttype","Can view content type"),
                     ("add_session","Can add session"),
                     ("change_session	","Can change session"),
                     ("delete_session","Can delete session"),
                     ("view_session","Can view session"),
                     ("add_products","Can add products"),
                     ("change_products","Can change products"),
                     ("delete_products","Can delete products"),
                     ("view_products","Can view products"),
                     ("add_address","Can add address"),
                     ("change_address	","Can change address"),
                     ("delete_address","	Can delete address"),
                     ("view_address","Can view address"),
                     ("add_cart","Can add cart"),
                     ("change_cart","Can change cart"),
                     ("delete_cart","Can delete cart"),
                     ("view_car","Can view cart"),
                     ("add_orders","Can add orders"),
                     ("change_orders","Can change orders"),
                     ("delete_orders","Can delete orders"),
                     ("view_orders","Can view orders"),

                     ("add_promotion","Can add promotion"),
                     ("change_promotion","Can change promotion"),
                     ("delete_promotion"	,"Can delete promotion"),
                     ("view_promotion	Can" ,"view promotion"),
)

    def __str__(self):
        return self.username+str(self.id)

class Products(models.Model):
    name=models.CharField(max_length=32)
    quantity=models.IntegerField(default=0)
    price = models.DecimalField(max_digits=5, decimal_places=2,default=0)
    img=models.ImageField(upload_to='static/img/product/')
    introduction=models.CharField(max_length=128)
    popularity=models.IntegerField(default=0)
    sold=models.IntegerField(default=0)

    def __str__(self):
        return self.name+str(self.id)

class Promotion(models.Model):
    productID=models.ForeignKey('shoppingCart.Products',on_delete=models.CASCADE)
    discount=models.DecimalField('Discount (%)',max_digits=2,decimal_places=0)
    promotionNum=models.CharField(max_length=5,unique=True)
    startDate=models.DateTimeField('Start Date',default = timezone.now)
    expireDate=models.DateTimeField('Expire Date',default = timezone.now)

class Cart(models.Model):
    # on_delete: 联级删除，即主表中数据删除后，附表中的数据也会删除
    # fields.E300: 跨模块的表 外键之前要加上表的名称
    userID=models.ForeignKey('shoppingCart.User',on_delete=models.CASCADE)
    productID=models.ForeignKey('shoppingCart.Products',on_delete=models.CASCADE)
    productName=models.CharField(max_length=64)
    quantity=models.IntegerField()

class Address(models.Model):
    # on_delete: 联级删除，即主表中数据删除后，附表中的数据也会删除
    # fields.E300: 跨模块的表 外键之前要加上表的名称
    userID=models.ForeignKey('shoppingCart.User', on_delete=models.CASCADE)
    state=models.CharField(max_length=32)
    city=models.CharField(max_length=32)
    detailAddress=models.CharField(max_length=128)
    address=models.CharField(max_length=32)

class Orders(models.Model):
    userID = models.ForeignKey('shoppingCart.User', on_delete=models.CASCADE)
    productName = models.CharField(max_length=64)
    quantity = models.IntegerField()
    address = models.CharField(max_length=128)
    addressee = models.CharField(max_length=128)
    price = models.IntegerField(default=0)




