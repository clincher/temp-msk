#-*- coding: utf-8 -*-
from django.contrib import admin
from django.db.models.aggregates import Max
from django.http import HttpResponse
from models import *

js_admin  = (
    '{0}ckeditor/ckeditor.js'.format(settings.STATIC_URL),
    '{0}js/ckeditor.js'.format(settings.STATIC_URL),
    )

class OrderProductInline(admin.TabularInline):
    model = Order.services.through
    
class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderProductInline,]

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    
class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImageInline]
    
    class Media:
        js = js_admin

    exclude = ["position"]


    def save_model(self, request, obj, form, change):
        if not change:
            query = Product.objects.filter(productgroup=obj.productgroup).aggregate(Max('position'))
            max = query['position__max']
            if max is None:
                obj.position = 0
            else:
                obj.position = max +1

            productgroup = obj.productgroup
            while productgroup is not None:
                productgroup.products_count += 1
                productgroup.save()
                productgroup = productgroup.productgroup

        else:
            obj_before = Product.objects.get(id=obj.id)
            obj.position = obj_before.position

        obj.save()

    def delete_model(self, request, obj):
        productgroup = obj.productgroup
        while productgroup is not None:
            productgroup.products_count = productgroup.products_count - 1
            productgroup.save()
            productgroup = productgroup.productgroup
        obj.delete()

class ProductGroupAdmin(admin.ModelAdmin):
    class Media:
        js = js_admin

    exclude = ["position", "products_count"]


    def save_model(self, request, obj, form, change):
        if not change:
            max = ProductGroup.objects.filter(productgroup=obj.productgroup).aggregate(Max('position'))['position__max']
            if max is None:
                obj.position = 0
            else:
                obj.position = max +1
        else:
            obj_before = ProductGroup.objects.get(id=obj.id)
            obj.position = obj_before.position

        obj.save()

def savesort(modeladmin, request, queryset):

    newsort = request.POST['array_string'].split("&")
    objects = modeladmin.model.objects

    for i in range(len(newsort)):
        link = objects.get(id=int(newsort[i].replace("page_id=", "")))
        link.position = i
        link.save()

    return HttpResponse('Новая сортировка сохранена')

admin.site.add_action(savesort, 'savesort')


admin.site.register(Product, ProductAdmin)
admin.site.register(ProductGroup, ProductGroupAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Unit)