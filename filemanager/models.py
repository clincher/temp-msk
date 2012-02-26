#-*- coding: utf-8 -*-
from django.db import models

# Create your models here.
class Filemanager(models.Model):
    
    class Meta:
        verbose_name = u"Менеджер файлов"
        verbose_name_plural = u"Менеджер файлов"
        permissions = (
            ("edit", "Can edit"),
        )
