from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from djnago.core.urlresolvers import reverse
from ergo_info.models import Allergy, UserToAllergy, Drug, UserToDrug, Immunization, UserToImmunization, History, FamilyHistory, Provider
from django.template import RequestContext
from django.views.decorators.csrf import csrf_protect

import json


def allergies_get(request):
    return render_to_response('allergies.html')
    
def allergies_post(request):
    return render_to_response('allergies-edit.html')
    
def drugs_get(request):
    return render_to_response('drugs.html')
    
def drugs_post(request):
    return render_to_response('drugs-edit.html')
    
def vaccines_get(request):
    return render_to_response('vaccines.html')
    
def vaccines_post(request):
    return render_to_response('vaccines-edit.html')
    
def history_conditions_get(request):
    return render_to_response('conditions.html')
    
def history_conditions_post(request):
    return render_to_response('conditions-edit.html')
    
def history_accidents_get(request):
    return render_to_response('accidents.html')
    
def history_accidents_post(request):
    return render_to_response('accidents-edit.html')
    
def history_hospitalization_get(request):
    return render_to_response('hospital.html')
    
def history_hospitalization_post(request):
    return render_to_response('hospital-edit.html')
    
def history_family_get(request):
    return render_to_response('family-history.html')
    
def history_family_post(request):
    return render_to_response('family-history-edit.html')
    
def providers_get(request):
    return render_to_response('providers.html')
    
def providers_post(request):
    return render_to_response('providers-edit.html')

