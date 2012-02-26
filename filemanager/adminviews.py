#-*- coding: utf-8 -*-
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.template import Context, loader
from django.contrib.auth.decorators import permission_required
from django import template


@permission_required('filemanager.change_filemanager',login_url='/admin')
def index(request):
    register = template.Library()
    return render_to_response('filemanager.html',
            {
                'title': u"Менеджер файлов",
                'base_root': '/admin',
            },
            context_instance=RequestContext(request))

@permission_required('filemanager.change_filemanager',login_url='/admin')
def popap(request):
    return render_to_response('filemanager_popup.html',
            {
                'title': u"Менеджер файлов",
                'base_root': '/admin',
            },
            context_instance=RequestContext(request))
