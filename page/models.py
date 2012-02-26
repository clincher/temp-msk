#-*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

# Create your models here.
from thumbs import ImageWithThumbsField

class Page(models.Model):
    class Meta:
        verbose_name = u"Страница"
        verbose_name_plural = u"Страницы"
    title = models.CharField(u'Заголовок', max_length=255,
        help_text=u'Внимание заголовок будет отображаться на странице при просмотре.')
    menu_title = models.CharField(u'Заголовок в меню', blank=True, max_length=255,
        help_text=u'Внимание заголовок будет отображаться в меню')
    content = models.TextField(u'Содержание')
    url = models.CharField(u'Aдрес', unique=True, max_length=255,
        help_text=u"""ТОЛЬКО латиницей, без пробелов и "НЕПРАВИЛЬНЫХ" символов
         типа "слешей", "собачек", "амперсантов" и. Слова index, search, sitemap
         ,how_to_buy, about, contacts уже заняты! index - это текст на ГЛАВНУЮ
         страницу!!!!""")
    keywords = models.CharField(u'Ключевые слова в метатеге', max_length=255,
        null=True, blank=True)
    meta_description = models.CharField(u'Метатег "description"',
        max_length=255, null=True, blank=True)

    def __unicode__(self):
        if self.menu_title:
            return self.menu_title
        return self.title
    

class News(models.Model):
    class Meta:
        verbose_name = u"Новость"
        verbose_name_plural = u"Новости"
        unique_together = ("date", "url")

    ordering = ["-date"]

    title = models.CharField(u'Заголовок', max_length=255)
    date = models.DateField(u'Дата', default=datetime.now());
    smallcontent = models.TextField(u'Вводный текст')
    content = models.TextField(u'Основное содержание')
    url = models.SlugField(u"Адрес", null=True, blank=True)
    keywords = models.CharField(u'Ключевые слова в метатеге', max_length=255,
        null=True, blank=True)
    
    def __unicode__(self):
        return self.title

    @models.permalink
    def get_url(self):
        url = str(self.url) if self.url else ""
        return 'news_read', (str(self.date), url)
    

class Message(models.Model):
    class Meta:
        verbose_name = u"Сообщение"
        verbose_name_plural = u"Сообщения"
    sender = models.CharField(u'Имя и Фамилия', max_length=255)
    email = models.EmailField(u'Адрес электронной почты', max_length=255)
    content = models.TextField(u'Содержание')
    date = models.DateTimeField(u'Дата', auto_now=True)
    
    def __unicode__(self):
        return '{0} {1}'.format(self.sender, str(self.date))


class Link(models.Model):
    class Meta:
        verbose_name = u"Ссылка"
        verbose_name_plural = u"Ссылки"
    page = models.ForeignKey(Page, related_name="page_links")

    def __unicode__(self):
        return self.page.__unicode__()


class FootMenuLink(Link):
    class Meta:
        verbose_name = u"Ссылка внизу"
        verbose_name_plural = u"Ссылки внизу"
        ordering = ['position']
    position = models.IntegerField(u'Позиция', null=True, blank=True)

class LeftMenuLink(Link):
    class Meta:
        verbose_name = u"Ссылка слева"
        verbose_name_plural = u"Ссылки слева"
        ordering = ['position']

    position = models.IntegerField(u'Позиция', null=True, blank=True)