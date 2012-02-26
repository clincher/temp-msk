#-*- coding: utf-8 -*-
from page.models import Page, LeftMenuLink, FootMenuLink
from shop.models import Product, ProductGroup
from django.template import Library
from django.contrib.contenttypes.models import ContentType

register = Library()

def groupslist():
    ct = ContentType.objects.get_for_model(ProductGroup)
    return {'results': ProductGroup.objects.filter(productgroup=None), 'ct': ct}
groupslist = register.inclusion_tag('admin/sorted/change_list_results.html')(groupslist)


def productslist():
    return {
        'results': Product.objects.filter(productgroup=None),
        'ct': ContentType.objects.get_for_model(Product),
        "groups": ProductGroup.objects.filter(productgroup=None)
    }
productslist = register.inclusion_tag('admin/shop/product/change_list_results.html')(productslist)


def parent_links(link, ct):
    results = []
    while link is not None:
        results.insert(0, link)
        link = link.productgroup
    return {'results': results, 'ct': ct}
parent_links = register.inclusion_tag('admin/shop/parent_links.html')(parent_links)



def leftmenulinklist():
    return {'results': LeftMenuLink.objects.all(), 'ct': ContentType.objects.get_for_model(LeftMenuLink)}
leftmenulinklist = register.inclusion_tag('admin/sorted/change_list_results.html')(leftmenulinklist)

def footmenulinklist():
    return {'results': FootMenuLink.objects.all(), 'ct': ContentType.objects.get_for_model(FootMenuLink)}
footmenulinklist = register.inclusion_tag('admin/sorted/change_list_results.html')(footmenulinklist)

@register.simple_tag
def link_to_children_links(link, metaname):
    if getattr(link, metaname).all():
        return '<a onclick="get_sub_elements(%d)" class="link_to_children_links">Подгруппы</a>' % link.pk
    return ""


def submit_row_page(context):
    """
    Displays the row of buttons for delete and save.
    """
    opts = context['opts']
    change = context['change']
    is_popup = context['is_popup']
    save_as = context['save_as']
    return {
        'onclick_attrib': (opts.get_ordered_objects() and change
                           and 'onclick="submitOrderForm();"' or ''),
        'show_delete_link': (not is_popup and context['has_delete_permission']
                             and (change or context['show_delete']) and context["original"].url not in ["index", "products", "search", "contacts", "sitemap"]),
        'show_save_as_new': not is_popup and change and save_as,
        'show_save_and_add_another': context['has_add_permission'] and
                                     not is_popup and (not save_as or context['add']),
        'show_save_and_continue': not is_popup and context['has_change_permission'],
        'is_popup': is_popup,
        'show_save': True
    }
submit_row_page = register.inclusion_tag('admin/page/page/submit_line.html', takes_context=True)(submit_row_page)