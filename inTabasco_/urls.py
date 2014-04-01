from django.conf.urls import patterns, include, url
from django.conf import settings
from django.views.generic.base import TemplateView

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'inTabasco_.views.home', name='home'),
    # url(r'^inTabasco_/', include('inTabasco_.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^', include('inTabasco_.apps.inTabasco.urls')),
    url(r'^', include('inTabasco_.apps.Login.urls')),
    url(r'^', include('inTabasco_.apps.correos.urls')),
    url(r'^', include('inTabasco_.apps.administracion.urls')),
    url(r'^', include('inTabasco_.apps.autocompletable.urls')),
    url(r'^admin/', include(admin.site.urls)),

)

if settings.DEBUG:
# static files (images, css, javascript, etc.)
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': settings.MEDIA_ROOT}))
if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^404/$', TemplateView.as_view(template_name="404.html")),
    )
