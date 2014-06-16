from django.conf.urls import patterns, include, url
from django.conf.urls import *
from django.conf import settings
from django.conf.urls.static import static
#from deliverkindle.main.feed import BookFeed
from django.contrib import admin

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

admin.autodiscover()
urlpatterns = patterns('',
    (r'^$','deliverkindle.main.views.index'),
    (r'^category/$','deliverkindle.books.views.category_list'),
    (r'^category/(\d+)/$','deliverkindle.books.views.category_book_list'),
    (r'^category/(\d+)/p(\d{1,10})/$','deliverkindle.books.views.category_book_list'),
	(r'^books/',include('deliverkindle.books.urls')),
    (r'^comments/', include('django.contrib.comments.urls')),
    #(r'^favorites/', include('deliverkindle.favorites.urls')),
    (r'^main/',include('deliverkindle.main.urls')),
    (r'^accounts/',include('deliverkindle.accounts.urls')),
    (r'^home/',include('deliverkindle.home.urls')),
    (r'^topic/',include('deliverkindle.topic.urls')),
    (r'^about/','deliverkindle.main.views.about'),
    (r'^disclaimer/','deliverkindle.main.views.disclaimer'),
    (r'^contact/','deliverkindle.main.views.contact'),
    (r'^partner/','deliverkindle.main.views.partner'),
    (r'^subscribe/$','deliverkindle.main.views.subscribe'),
    #(r'^feeds/$',BookFeed()),
    (r'^admin/', admin.site.urls),
	#(r'^static/(?P<path>.*)$','django.views.static.serve',{'document_root':settings.ROOT_PATH}),
	
	#(r'^(?P<path>.*)$','django.views.static.serve',{'document_root':settings.ROOT_PATH}),

    # Examples:
    # url(r'^$', 'deliverkindle.views.home', name='home'),
    # url(r'^deliverkindle/', include('deliverkindle.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
