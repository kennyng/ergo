from django.conf.urls import patterns, url

from ergo_info.views import providers
from ergo_info.views import immunizations
from ergo_info.views import drugs


urlpatterns = patterns('',
    # Providers
    url(r'^providers/$', providers.index),
    url(r'^providers/edit/$', providers.edit_form),
    url(r'^providers/edit/post/$', providers.edit_providers),

    # Immunizations
    url(r'^shots/$', immunizations.index),
    url(r'^shots/add/$', immunizations.dialog_add),
    url(r'^shots/add/post/$', immunizations.add_vaccine),
    url(r'^shots/remove/$', immunizations.dialog_remove),
    url(r'^shots/remove/post/$', immunizations.remove_vaccine),

    # Drugs
    url(r'^drugs/$', drugs.index),
    url(r'^drugs/add/$', drugs.dialog_add),
    url(r'^drugs/add/post/$', drugs.add_drug),
    url(r'^drugs/remove/$', drugs.dialog_remove),
    url(r'^drugs/remove/post/$', drugs.remove_drug),
)