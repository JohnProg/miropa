from django.conf.urls import patterns, include, url

from django.contrib import admin
from miropa import settings

admin.autodiscover()
urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'miropa.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^', include('apps.login.urls')),
    url(r'^people/', include('apps.people.urls')),
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': settings.MEDIA_ROOT, }),
    url(r'^grappelli/', include('grappelli.urls')), # grappelli URLS
    url(r'^admin/', include(admin.site.urls)),
)

