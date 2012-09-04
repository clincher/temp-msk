#-*- coding: utf-8 -*-

from django.db import models
from django.utils.html import strip_tags
from page.models import Page
from thumbs import ImageWithThumbsField
from django.conf import settings

class Unit(models.Model):
    class Meta:
        verbose_name = u"Единица измерения стоимости"
        verbose_name_plural = u"Единицы измерения стоимости"
    
    title = models.CharField(u"Название", max_length=255)
    
    def __unicode__(self):
        return self.title


#    ALTER TABLE `shop_productgroup` ADD `products_count` int( 11 ) NOT NULL DEFAULT 0 AFTER `position`;
#   ALTER TABLE `shop_product` ADD `property` TEXT NOT NULL  AFTER `productgroup` ,

class ProductGroup(models.Model):
    class Meta:
        verbose_name = u"Группа товаров"
        verbose_name_plural = u"Группы товаров"
        ordering = ["position"]

    title = models.CharField(u"Название группы", max_length=255)
    description = models.TextField(u'Описание группы')
    productgroup = models.ForeignKey("shop.ProductGroup", related_name="sub_groups", null=True, blank=True)
    image = models.ImageField(u"Изображение", upload_to='uploads/groups')
    position = models.IntegerField(u"Позиция в списке")
    products_count = models.IntegerField(u"Товаров в группе", default=0, blank=True)
    keywords = models.CharField(u"Ключевые слова", max_length=255, null=True, blank=True)

    def __unicode__(self):
        return self.title

    def get_image_url(self):
        return "%s%s" %(settings.MEDIA_URL, self.image)

    def get_page(self):
        return Page(title=self.title, keywords=self.keywords, meta_description=strip_tags(self.description))

class Product(models.Model):
    class Meta:
        verbose_name = u"Товар"
        verbose_name_plural = u"Товары"
        ordering = ["position"]
        
    title = models.CharField(u"Название товара", max_length=255)
    productgroup = models.ForeignKey("shop.ProductGroup", related_name="group_products", null=True, blank=True)
    property = models.TextField(u'Характеристика', blank=True)
    description = models.TextField(u'Описание товара', blank=True)
    price = models.FloatField(u'Стоимость', default=0.0, help_text=u'Разделитель десятичной дроби - точка (.)')
    unit = models.ForeignKey(Unit, related_name="unit_products")
    load = models.IntegerField(u"Загрузка", default=1)
    position = models.IntegerField(u"Позиция в списке")
    keywords = models.CharField(u'Ключевые слова в метатеге', max_length=255, null=True, blank=True)
    meta_description = models.CharField(u'Метатег "description"', max_length=255, null=True, blank=True)

    def __unicode__(self):
        return self.title

    def get_image(self):
        try:
            return self.product_images.all()[0]
        except :
            return None

    def get_page(self):
        return Page(title=self.title, keywords=self.keywords, meta_description=self.meta_description)


    
class ProductImage(models.Model):
    class Meta:
        verbose_name = u"Скриншот"
        verbose_name_plural = u"Скриншоты"
        
    title = models.CharField(u"Название", max_length=255, blank=True, null=True)
    image = ImageWithThumbsField(upload_to='uploads/products', sizes=((95, 95), (150, 150), (300,300)) )
    service = models.ForeignKey(Product, related_name='product_images')
    
    def __unicode__(self):
        return self.title
    
    
class Order(models.Model):
    class Meta:
        verbose_name = u"Заказ"
        verbose_name_plural = u"Заказы"

    company = models.CharField(u'Организация', max_length=255, null=True)
    name = models.CharField(u'Контактное лицо', max_length=255, null=True)
    services = models.ManyToManyField(Product, related_name='order_products', through='OrderCount')
    date = models.DateTimeField(u'Дата и время', auto_now=True)
    phone = models.CharField(u'Телефон', max_length=255, null=True)
    email = models.EmailField(u'Эл. почта', max_length=255, null=True)
    description = models.TextField(u'Примечание к заявке', blank=True)
    
    def __unicode__(self):
        return self.name +' '+ str(self.date)

    
class OrderCount(models.Model):
    class Meta:
        verbose_name = u"Количество"
        verbose_name_plural = u"Количества"

    product = models.ForeignKey(Product, related_name='count_product')
    order = models.ForeignKey(Order, related_name='count_order')
    count = models.IntegerField(u'Количество', default=1)    
    
    def __unicode__(self):
        return self.product.title +' '+self.order.company


#class Link(models.Model):
#    class Meta:
#        verbose_name = u"Ссылка"
#        verbose_name_plural = u"Ссылки"
#    product = models.ForeignKey(Product, related_name="page_links")



#class HotOfferLink(Link):
#    class Meta:
#        verbose_name = u"Ссылка актуальной услуги"
#        verbose_name_plural = u"Ссылки актуальных услуг"
#    smalldescription = models.CharField(u"Краткое описание", max_length=255)
#    price = models.CharField(u"Цена", max_length=255)
#
#    def __unicode__(self):
#        return self.page.title

#
def get_model_manager_by_type(type):
    if type == 'productgroup':
        return ProductGroup.objects
    if type == 'product':
        return Product.objects