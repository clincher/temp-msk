#-*- coding: utf-8 -*-
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.contrib import messages
from django.conf import settings

from page.views import render_to
from models import Product, OrderCount, Order, ProductGroup
from forms import OrderForm
from page.models import Page
from urllib import unquote
import json

@render_to('shop/group.html')
def group(request, id=None):

    print ProductGroup.objects.filter(productgroup=None)

    if id:
        group = get_object_or_404(ProductGroup, id=id)
        groups = group.sub_groups.all()
        products = group.group_products.all()
        page = group.get_page()
    else:
        page = Page.objects.get(url="products")
        group = ProductGroup(title=u"Прайс-лист", description="", pk="")
        groups = ProductGroup.objects.filter(productgroup=None)
        products = Product.objects.filter(productgroup=None)

    return {'group': group, "groups": groups, "products": products, 'p':page}


@render_to('shop/product.html')
def product(request, id):
    product = get_object_or_404(Product, id=id)
    return {"product": product, "product_images": product.product_images.all(), "p":product.get_page()}

@render_to('shop/order.html')
def order(request):

    cookie_order = unquote(request.COOKIES.get("order", "{}"))
    order_items = json.loads(cookie_order)
    order_products = Product.objects.filter(id__in=order_items.keys())

    if request.method == "POST":
        form = OrderForm(request.POST)
        response = HttpResponseRedirect("/order")
        if form.is_valid():
            try:
                order=form.save(commit=False)
                order.save()
                ocs = []
                total = 0;
                for product in order_products:
                    oc = OrderCount(product=product, order=order, count=int(order_items[u"%d" % product.pk]['order_num'])*product.load)
                    oc.save()
                    oc.summ = order_items[u"%d" % product.pk]['order_summ']
                    total += oc.summ
                    ocs.append(oc)
                message = render_to_string('order_email.txt', {"products": ocs, "order": order, "total": total})
                send_to = [manager[1] for manager in settings.MANAGERS]
                email = EmailMessage(u'Заказ на сайте', message, 'temp <robot@temp-msk.ru>', to=send_to)
                email.send()
                messages.success(request, u'Ваша заявка отправлена специалистам компании.')
                response.delete_cookie("order")
            except :
                messages.error(request, u'При отправке заявки произошла ошибка. Пожалуйста, повторите попытку позднее.')

            return response
    else:
        form = OrderForm()

    return {'form':form, "products": order_products, "p": Page.objects.get(url="order")}