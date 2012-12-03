from django.conf.urls import patterns, url

from ergo_info.views import providers
from ergo_info.views import immunizations
from ergo_info.views import drugs
from ergo_info.views import allergies
from ergo_info.views import history


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
    url(r'^drugs/prescription/$', drugs.prescription_index),
    url(r'^drugs/otc/$', drugs.otc_index),
    url(r'^drugs/misc/$', drugs.misc_index),
                       
    url(r'^drugs/add/$', drugs.dialog_add),
    url(r'^drugs/add/post/$', drugs.add_drug),
    url(r'^drugs/remove/$', drugs.dialog_remove),
    url(r'^drugs/remove/post/$', drugs.remove_drug),

    # Allergies
    url(r'^allergies/drug/$', allergies.drug_index),
    url(r'^allergies/diet/$', allergies.diet_index),
    url(r'^allergies/misc/$', allergies.misc_index),

    url(r'^allergies/add/$', allergies.dialog_add),
    url(r'^allergies/add/post/$', allergies.add_allergy),
    url(r'^allergies/remove/$', allergies.dialog_remove),
    url(r'^allergies/remove/post/$', allergies.remove_allergy),

    # A/B test
    url(r'^allergies/listview/$', allergies.listview_index),
    url(r'^allergies/listview/add/$', allergies.listview_dialog_add),
    url(r'^allergies/listview/add/post/$', allergies.listview_add_allergy),
    url(r'^allergies/listview/remove/$', allergies.listview_dialog_remove),
    url(r'^allergies/listview/remove/post/$', allergies.listview_remove_allergy),

    # History
    url(r'^history/user/$', history.user_index),
    url(r'^history/entry/$', history.entry_display),
    
    url(r'^history/user/add/$', history.user_add_form),
    url(r'^history/user/add/post/$', history.add_user_history),
    url(r'^history/user/edit/$', history.user_edit_form),
    url(r'^history/user/edit/post/$', history.edit_user_history),
    url(r'^history/user/remove/$', history.remove_user_history),
    
    url(r'^history/family/$', history.family_index),
    url(r'^history/family/add/$', history.family_add_dialog),
    url(r'^history/family/add/post/$', history.add_family_history),
    url(r'^history/family/remove/$', history.family_remove_dialog),
    url(r'^history/family/remove/post/$', history.remove_family_history),
)