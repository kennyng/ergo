from django.conf.urls import patterns, url
from ergo_contacts import views

urlpatterns = patterns('',
    url(r'^$', views.contacts_index),
    url(r'^add/$', views.contacts_add_form),
    url(r'^add/post/$', views.add_contact),
    url(r'^edit/$', views.contacts_edit_form),
    url(r'^edit/update_post/$', views.update_contact),
    url(r'^edit/remove_post/$', views.remove_contact),
)