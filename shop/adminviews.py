#-*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.decorators import permission_required
from models import ProductGroup, get_model_manager_by_type
from django.contrib.contenttypes.models import ContentType


#@permission_required() productsview
from shop.models import Product

def groupsview(request, id):

    ct = ContentType.objects.get(app_label="shop", model="productgroup")
    model_class = ct.model_class()

    metaname = "sub_groups"

    parent = model_class.objects.get(id=id) if id else None
    results = model_class.objects.filter(productgroup__id=id)
    return render_to_response('admin/sub_links.html',
        {
            "ct": ct,
            "metaname": metaname,
            "parent": parent,
            'results': results
        },
        context_instance=RequestContext(request))

def groupsnavigate(request, id):

    ct = ContentType.objects.get(app_label="shop", model="productgroup")
    model_class = ct.model_class()

    metaname = "sub_groups"

    parent, current_id = (model_class.objects.get(id=id), id) if id else (None, "")
    results = model_class.objects.filter(productgroup__id=id)
    return render_to_response('admin/shop/productgroup/navigate.html',
            {
            "ct": ct,
            "metaname": metaname,
            "parent": parent,
            'results': results,
            'current_id': current_id
        },
        context_instance=RequestContext(request))

def productsview(request, id):


    ct = ContentType(app_label="shop", model="product")

    parent = ProductGroup.objects.get(id=id) if id else None
    results = Product.objects.filter(productgroup__id=id)

    groups = ProductGroup.objects.filter(productgroup__id=id)
    return render_to_response('admin/shop/product/products.html',
            {
            "ct": ct,
            "parent": parent,
            "groups" : groups,
            'results': results
        },
        context_instance=RequestContext(request))