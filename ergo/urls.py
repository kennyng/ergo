from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()

from ergo import settings


urlpatterns = patterns('',
    url(r'^$', 'ergo.views.index', name='index'),
    url('^accounts/', include('registration.backends.default.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^profile/', include('ergo_users.urls')),
    url(r'^contacts/', include('ergo_contacts.urls')),
    url(r'^info/', include('ergo_info.urls')),

    url(r'^drugs/otc/$', 'ergo.views.drugs_otc_get', name='drugs_otc_display'),
    url(r'^drugs/prescription/$', 'ergo.views.drugs_prescription_get', name='drugs_prescription_display'),
    url(r'^drugs/misc/$', 'ergo.views.drugs_misc_get', name='drugs_misc_display'),
    url(r'^allergies/drug/$', 'ergo.views.allergies_drug_get', name='allergies_drug_get'),
    url(r'^allergies/diet/$', 'ergo.views.allergies_diet_get', name='allergies_diet_get'),
    url(r'^allergies/misc/$', 'ergo.views.allergies_misc_get', name='allergies_misc_get'),

    # url(r'^ergo/', include('ergo.foo.urls')),
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
)

if settings.DEBUG:
        urlpatterns += patterns('',
            (r'^static/(?P<path>.*)$', 'django.views.static.serve',
             {'document_root': settings.STATIC_ROOT, 'show_indexes': True}),
        )
