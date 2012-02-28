#-*- coding: utf-8 -*-
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.conf import settings
from django.utils.html import strip_tags
from django.contrib import messages

from forms import MessageForm
from models import Page, News

from datetime import datetime
from page.forms import DefinitionErrorList
from shop.models import ProductGroup


def render_to(tmpl):
    def renderer(func):
        def wrapper(request, *args, **kw):
            output = func(request, *args, **kw)
            if not isinstance(output, dict):
                return output
            output['settings'] = settings
            return render_to_response(tmpl, output, context_instance=RequestContext(request))
        return wrapper
    return renderer


@render_to('home.html')
def home(request):
    return {'p': get_object_or_404(Page, url='index'), 'groups': ProductGroup.objects.filter(productgroup=None)}

@render_to('contacts.html')
def contacts(request):
    return {'p': get_object_or_404(Page, url='contacts'), 'MAPS_API_KEY': settings.MAPS_API_KEY}

@render_to('search.html')
def error404(request):
    return {'p':Page(title=u'Такой страницы не найдено', content=u'Такой страницы не существует. Воспользуйтесь поиском по сайту')}
    
@render_to('search.html')
def error403(request):
    return {'p':Page(title=u'Недостаточно прав для совершения операции', content=u'Недостаточно прав для совершения операции.')}

@render_to('search.html')
def error500(request):
    return {'p':Page(title=u'Ошибка сервера', content=u'Произошла серверная ошибка.')}

@render_to('search.html')
def search(request):
    return {'p':Page.objects.get(url="search"), 'query': request.GET.get('query', ''), 'SEARCH_API_KEY': settings.SEARCH_API_KEY}

@render_to('page.html')
def page(request, url):
    return {'p':get_object_or_404(Page, url=url)}

@render_to('newsall.html')
def newslist(request, page=1):
    if(page is None):
        page = 1
    else:
        page = int(page)
    paginator = Paginator(News.objects.filter(date__lte=datetime.now()), 5)
    try:
        newspage = paginator.page(page)
    except PageNotAnInteger:
        newspage = paginator.page(1)
    except EmptyPage:
        newspage = paginator.page(paginator.num_pages)

    return {
        'newspage': newspage,
        'p': Page(title="Новости", url="news"),
        }

@render_to('news.html')
def newsread(request, newsdate, url):
    news = get_object_or_404(News, date=newsdate, url=url)
    return {'news':news, "p": Page(title=news.title, keywords=news.keywords, meta_description=strip_tags(news.smallcontent))}

@render_to('sitemap.html')
def sitemap(request):
    return {'p': get_object_or_404(Page, url='sitemap'),
            "pages": Page.objects.all().exclude(url="order"),
            "groups": ProductGroup.objects.filter(productgroup=None)}

@render_to('blocks/message-form.html')
def message(request):
    if request.method == "POST":
        form = MessageForm(request.POST, error_class = DefinitionErrorList)
        if form.is_valid():
            try:
                msg=form.save(commit=False)
                msg.save()
                message = render_to_string('message_email.txt', {'msg':msg})
                send_to = [manager[1] for manager in settings.MANAGERS]
                email = EmailMessage(u"Сообщение с сайта temp-msk", message, u'ТЕМП <no-reply@temp-msk.ru>', send_to)
                email.send()
                messages.success(request, u'Сообщение отправлено специалистам компании')
                return {'form': MessageForm()}
            except :
                messages.error(request, u'При отправке произошла ошибка. Пожалуйста, повторите попытку позднее.')
    else:
        form = MessageForm()

    return {'form': form}