#-*- coding: utf-8 -*-
"""
Forms and validation code for user registration.

"""

from models import Order, OrderCount
from django import forms
from django.utils.translation import ugettext_lazy as _
import random


        
class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        exclude = ('date','services')


class OrderCountForm(forms.Form):
    product = forms.CharField(max_length=0)

#    def save(self, commit=True):
#        order = super(OrderForm, self).save(commit=False)
#        if commit:
#            order.save()
#        return order
    
class DefinitionErrorList(forms.util.ErrorList):
    def __unicode__(self): 
        if not self: 
            return u'' 
        return u'<label class="error" style="display:block;">%s</label>' % '<br />'.join([u'<span>%s</span>' % e for e in self])   