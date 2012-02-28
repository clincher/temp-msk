#-*- coding: utf-8 -*-

from page.models import LeftMenuLink, News
from shop.models import ProductGroup
from django.template import Library
from datetime import datetime

register = Library()

def news_block():
    newses = News.objects.filter(date__lte=datetime.now())[:5]
    return {"newses": newses}
news_block = register.inclusion_tag('blocks/news.html')(news_block)


def leftmenulinks():
    return {"links": LeftMenuLink.objects.all()}
leftmenulinks = register.inclusion_tag('blocks/leftmenulinks.html')(leftmenulinks)

def footmenulinks():
    return {"links": LeftMenuLink.objects.all()}
footmenulinks = register.inclusion_tag('blocks/footmenulinks.html')(footmenulinks)

def left_menu(group=None):

    head_group = group
    if group:
        parent = group.productgroup
        while parent is not None:
            head_group = parent
            parent = parent.productgroup

    groups = ProductGroup.objects.filter(productgroup=None)
    for gr in groups:
        gr.head = False
        if head_group and gr.pk == head_group.pk:
            gr.head = True
    return {"groups": groups}
left_menu = register.inclusion_tag('blocks/left-menu.html')(left_menu)

def navigation(group):
    groups = [group]
    parent = group.productgroup
    while parent is not None:
        groups.insert(0, parent)
        parent = parent.productgroup

    return {'groups':groups}
navigation = register.inclusion_tag('blocks/navigation.html')(navigation)

def productlist(group):
    result = {"group": group, "products": []}
    if group.pk:
        result["products"] = group.group_products.all()
    return result
productlist = register.inclusion_tag('shop/product-list.html')(productlist)


def sub_groups(groups):
    return {"groups": groups}
sub_groups = register.inclusion_tag('blocks/sub_groups.html')(sub_groups)