from django.contrib import admin
from .models import *
# Register your models here.

class UserAdmin(admin.ModelAdmin):
    list_display = ('id','username')

class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'category','title','created_at','is_closed')

admin.site.register(User,UserAdmin)
admin.site.register(Product,ProductAdmin)
admin.site.register(Bid)
admin.site.register(Comment)
admin.site.register(Watchlist)
admin.site.register(Result)
