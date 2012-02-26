#-*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.decorators import permission_required
from django.contrib.contenttypes.models import ContentType


#@permission_required() productsview

def linksview(request, model, id):

    ct = ContentType.objects.get(app_label="page", model=model)
    results = ct.model_class().objects.all()
    return render_to_response('admin/sub_links.html',
        {
            "ct": ct,
            "metaname": "",
            "parent": None,
            'results': results
        },
        context_instance=RequestContext(request))
