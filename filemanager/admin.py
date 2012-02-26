#-*- coding: utf-8 -*-
# filemanager/admin.py
from django.contrib import admin
from django.db import models


class Filemanager(models.Model):
    class Meta:
        verbose_name = u"Менеджер файлов"
        verbose_name_plural = u"Менеджер файлов"


class FilemanagerAdmin(admin.ModelAdmin):

    def get_model_perms(self, request):
        return {
            'add': False,
            'change': True,
            'delete': False,
        }


admin.site.register(Filemanager, FilemanagerAdmin)