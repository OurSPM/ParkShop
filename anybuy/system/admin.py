from django.contrib import admin
from system.models import *

# Register your models here.

class HomeShopAdvAdmin(admin.ModelAdmin):
    list_display = ('id','ShopID', 'AdvertisementContent', 'ApplyState')
    search_fields = ('id', 'AdvertisementContent')

class HomeCommodityAdvAdmin(admin.ModelAdmin):
    list_display = ('id', 'CommodityID', 'AdvertisementContent', 'ApplyState')
    search_fields = ('id','AdvertisementContent')

class CommodityAdmin(admin.ModelAdmin):
    list_display = ('id', 'CommodityName', 'CommodityImage')
    search_fields = ('id', 'CommodityName', 'CommodityDescription')

class ShopOwnerAdmin(admin.ModelAdmin):
    list_display = ('id', 'SellerName','SellerTelephone','SellerEmail','SellerAddress')
    search_fields = ('id', 'SellerName', 'SellerTelephone','SellerEmail','SellerAddress')

class ShopAdmin(admin.ModelAdmin):
    list_display = ('id', 'SellerID','ShopName')
    search_fields = ('id', 'SellerID__SellerType','ShopName')

class CustomerAdmin(admin.ModelAdmin):
    list_display = ('id', 'CustomerAccount','CustomerPassword','CustomerName','CustomerTelephone','CustomerEmail','CustomerAddress')
    search_fields = ('id', 'CustomerAccount','CustomerPassword','CustomerName','CustomerTelephone','CustomerEmail','CustomerAddress')

class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'OrderListState')
    search_fields = ('id', )
#    search_fields = ('id', 'ShopOrderID__id', 'CustomerOrderID__id' )
#list_display = ('id', 'OrderListState','OrderListDate','OrderAmount','ShopOrderID','CustomerOrderID','CommodityID')
admin.site.register(HelpCenter)
admin.site.register(Seller, ShopOwnerAdmin)
admin.site.register(Shop, ShopAdmin)
admin.site.register(Commodity, CommodityAdmin)
admin.site.register(ShopAdv)
admin.site.register(CommodityAdv)
admin.site.register(HomeShopAdv, HomeShopAdvAdmin)
admin.site.register(HomeCommodityAdv, HomeCommodityAdvAdmin)
admin.site.register(Administrator)
admin.site.register(System)
admin.site.register(BlacklistSeller)
admin.site.register(Discount)
admin.site.register(ShopOrder)
admin.site.register(Customer,CustomerAdmin)
admin.site.register(OrderList,OrderAdmin)
#admin.site.register(OrderList)
admin.site.register(Comment)
admin.site.register(Cart)
admin.site.register(Favorite)
admin.site.register(CustomerOrder)
admin.site.register(BlacklistCustomer)
admin.site.register(Income)
