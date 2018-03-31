"""nineworldsdeep URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic import TemplateView
import core.views

urlpatterns = [
    #url(r'^$', core.views.index, name='index'), 
    #url(r'^$', TemplateView.as_view(template_name="bootstrap-index.html")),
    url(r'^$', core.views.index, name='index'),
    url(r'^sandbox/', TemplateView.as_view(template_name="bootstrap-index.html")),
    url(r'^admin/', admin.site.urls),
    url(r'^accounts/', include('django.contrib.auth.urls')),
    url(r'^documents/$', core.views.DocumentListView.as_view(), name='documents'),
    url(r'^documents/(?P<pk>\d+)$', core.views.DocumentDetailView.as_view(), name='document-detail'),
    url(r'^quotes/$', core.views.QuoteListView.as_view(), name='quotes'), 
    url(r'^quotes/(?P<pk>\d+)$', core.views.QuoteDetailView.as_view(), name='quote-detail'), #need to check ownership permissions, etc.
    url(r'^quotes/create/$', core.views.QuoteCreate.as_view(), name='quote-create'),
    url(r'^xml/download/$', core.views.xml_download, name='xml-download'),
    url(r'^xml/upload/$', core.views.xml_upload, name='xml-upload'),
    # url(r'^quotes/create/$', core.views.quote_entry, name='quote-create'),
    url(r'^quotes/(?P<pk>\d+)/update/$', core.views.QuoteUpdate.as_view(), name='quote-update'),
    url(r'^quotes/(?P<pk>\d+)/delete/$', core.views.QuoteDelete.as_view(), name='quote-delete'),
    url(r'^myquotes/$', core.views.QuotesPrivateForUserListView.as_view(), name='my-quotes'),
]
