from django.conf.urls import patterns, url
from ergo_users import views

urlpatterns = patterns('',
    url(r'^$', views.profile_index),
    url(r'^edit/$', views.profile_form),
    url(r'^edit/post/$', views.update_profile),
)