from django.conf.urls.defaults import patterns, include, url
from django.conf import settings

from django.contrib import admin
admin.autodiscover()

handler404 = 'page.views.error404'
handler403 = 'page.views.error403'
handler500 = 'page.views.error500'

urlpatterns = patterns('',
    (r'^$', 'page.views.home'),
    url(r'^index.html$', 'page.views.home', name='home'),
    url(r'^news$', 'page.views.newslist', name="news_main"),
    url(r'^news-(?P<page>\d+)$', 'page.views.newslist', name="news_page"),
    url(r'^news/(?P<newsdate>[-0-9]+)/(?P<url>[-\w]+)?$', 'page.views.newsread', name="news_read"),
    url(r'^contacts.html$', 'page.views.contacts', name='contacts'),
    (r'^media/(.*)$', 'django.views.static.serve',{'document_root': settings.MEDIA_ROOT}),
    (r'^media_admin/(.*)$', 'django.views.static.serve',{'document_root': '/Library/Python/2.6/site-packages/django/contrib/admin/media/'}),

    url(r'^products/(?P<id>\d+)?$', 'shop.views.group', name="price_list"),
    (r'^products.html$', 'shop.views.group'),
    url(r'^product/(?P<id>\d+)$', 'shop.views.product', name="product_link"),
    url(r'^order[/]', 'shop.views.order', name='order_link'),

    (r'^filemanager_connectors/', include('filemanager.connector.urls')),
    (r'^filemanager/', 'filemanager.adminviews.index'),
    (r'^admin/filemanager/', include('filemanager.urls')),
    (r'^admin/', include(admin.site.urls)),

    (r'^admin/shop/productgroups/(?P<id>\d+)?', "shop.adminviews.groupsview"),
    (r'^admin/shop/productgroups_navigate/(?P<id>\d+)?', "shop.adminviews.groupsnavigate"),
    (r'^admin/shop/products/(?P<id>\d+)?', "shop.adminviews.productsview"),

    (r'^admin/page/(?P<model>\w+)s/(?P<id>\d+)?', "page.adminviews.linksview"),

    url(r'^message$', 'page.views.message', name='message'),
    url(r'^search.html$', 'page.views.search', name='search'),
    url(r'^sitemap.html$', 'page.views.sitemap', name='sitemap'),
    url(r'^(?P<url>[-\w]+).html$', 'page.views.page', name='page_link'),
#    (r'^sitemap.xml$', 'django.contrib.sitemaps.views.sitemap', {'sitemaps': sitemaps}),
    (r'^robots.txt$', 'django.views.static.serve', {'path':"robots.txt",'document_root': settings.MEDIA_ROOT,'show_indexes': False }),
    (r'^favicon.ico$', 'django.views.static.serve', {'path':"images/favicon.ico",'document_root': settings.MEDIA_ROOT,'show_indexes': False }),
    url(r'^captcha/(?P<code>[\da-f]{32})/$', 'supercaptcha.views.draw'),
#   
)
