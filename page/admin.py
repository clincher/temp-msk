#-*- coding: utf-8 -*-
from django.conf import settings
from django.db.models.aggregates import Max
from models import News, Page, Message, LeftMenuLink, FootMenuLink
from django.contrib import admin

js_admin = js = (
    '{0}js/jquery.js'.format(settings.STATIC_URL),
    '{0}js/jquery-ui.min.js'.format(settings.STATIC_URL),
    '{0}ckeditor/ckeditor.js'.format(settings.STATIC_URL),
    '{0}js/ckeditor.js'.format(settings.STATIC_URL),
    )

class PageAdmin (admin.ModelAdmin):

    class Media:
        js = js_admin

    def delete_model(self, request, obj):
        if obj.url not in ["index", "products", "search", "contacts", "sitemap"]:
            obj.delete()

admin.site.register(Page, PageAdmin) 
admin.site.register(Message) 

class NewsAdmin (admin.ModelAdmin):
    list_display = ('title', 'date')
    
    class Media:
        js = js_admin

admin.site.register(News, NewsAdmin)


class LeftMenuLinkAdmin(admin.ModelAdmin):
    exclude = ["position"]

    class Media:
        js = js_admin

    def save_model(self, request, obj, form, change):
        if not change:
            max = LeftMenuLink.objects.all().aggregate(Max('position'))['position__max']
            if max is None:
                obj.position = 0
            else:
                obj.position = max +1
        else:
            obj_before = LeftMenuLink.objects.get(id=obj.id)
            obj.position = obj_before.position

        obj.save()

admin.site.register(LeftMenuLink, LeftMenuLinkAdmin)

class FootMenuLinkAdmin(admin.ModelAdmin):
    exclude = ["position"]

    class Media:
        js = js_admin

    def save_model(self, request, obj, form, change):
        if not change:
            max = FootMenuLink.objects.all().aggregate(Max('position'))['position__max']
            if max is None:
                obj.position = 0
            else:
                obj.position = max +1
        else:
            obj_before = FootMenuLink.objects.get(id=obj.id)
            obj.position = obj_before.position

        obj.save()

admin.site.register(FootMenuLink, FootMenuLinkAdmin)


#def savesort(modeladmin, request, queryset):
#
#    newsort = request.POST['array_string'].split("&")
##    model_class = ContentType.objects.get(app_label="page", model=request.POST.get('type')).model_class()
#    objects = modeladmin.objects
#
#    for i in range(len(newsort)):
#        link = objects.get(id=int(newsort[i].replace("page_id=", "")))
#        link.position = i
#        link.save()
#
#    return HttpResponse('Новая сортировка сохранена')
#
#admin.site.add_action(savesort, 'savesort')