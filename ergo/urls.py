from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()

from django.conf import settings
from django.conf.urls.static import static


urlpatterns = patterns('',
    url(r'^$', 'ergo.views.index', name='index'),
    url(r'^er/access/$', 'ergo.views.emergency_access'),
    url('^accounts/', include('registration.backends.default.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^profile/', include('ergo_users.urls')),
    url(r'^contacts/', include('ergo_contacts.urls')),
    url(r'^info/', include('ergo_info.urls')),


    # url(r'^ergo/', include('ergo.foo.urls')),
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
)

if settings.DEBUG:
        urlpatterns += patterns('',
            (r'^static/(?P<path>.*)$', 'django.views.static.serve',
             {'document_root': settings.STATIC_ROOT, 'show_indexes': True}),
        )

        urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

