from django.conf.urls import url, include
from django.contrib import admin

admin.autodiscover()

from spoons.views import *

from django.views.generic import TemplateView

urlpatterns = [

    url(r'^get/(?P<key>[:\.\-\w]+)', get),

    url(r'^search', search),
    url(r'^summary', summary),
    url(r'^sources', sources),

    url(r'^admin/', include(admin.site.urls)),

]
