from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.views.decorators.csrf import csrf_protect
from django.core.urlresolvers import reverse

from ergo_info.models import Drug, UserToDrug, Allergy, UserToAllergy


def index(request):
    if request.user.is_authenticated():
        # for authenticated (logged in) users
        return render_to_response('index.html')
    else:
        # for anonymous users
        return HttpResponseRedirect('/accounts/login/')
        

def drugs_otc_get(request):
    records = UserToDrug.objects.filter(user=request.user)
    cabinet = {}
    overflow = 0
    drugs = []
    for x in records:
        if x.drug.drug_category == 'otc':
            drug = {'drug_name': x.drug.drug_name, 'drug_img': x.drug.drug_img}
            drugs.append(drug)
    shelf = [drugs[i:i+3] for i in range(0, len(drugs), 3)]
    if (len(drugs) % 3) > 0:
        partition = len(shelf) - 1
        cabinet['fullshelf'] = shelf[:partition]
        overflow_shelf = shelf[partition:]
        cabinet['overflow'] = overflow_shelf
        overflow = len(overflow_shelf)
    else:
        cabinet['fullshelf'] = shelf
    extra_shelf = 4 - len(shelf)
    
    return render_to_response('info/drugs-otc.html', {'cabinet': cabinet, 'overflow': overflow, 'extra_shelf': extra_shelf}, RequestContext(request))

def drugs_prescription_get(request):
    records = UserToDrug.objects.filter(user=request.user)
    cabinet = {}
    overflow = 0
    drugs = []
    for x in records:
        if x.drug.drug_category == 'prescription':
            drug = {'drug_name': x.drug.drug_name, 'drug_img': x.drug.drug_img}
            drugs.append(drug)
    shelf = [drugs[i:i+3] for i in range(0, len(drugs), 3)]
    if (len(drugs) % 3) > 0:
        partition = len(shelf) - 1
        cabinet['fullshelf'] = shelf[:partition]
        overflow_shelf = shelf[partition:]
        cabinet['overflow'] = overflow_shelf
        overflow = len(overflow_shelf)
    else:
        cabinet['fullshelf'] = shelf
    extra_shelf = 4 - len(shelf)
    
    return render_to_response('info/drugs-prescription.html', {'cabinet': cabinet, 'overflow': overflow, 'extra_shelf': extra_shelf}, RequestContext(request))

def drugs_misc_get(request):
    records = UserToDrug.objects.filter(user=request.user)
    cabinet = {}
    overflow = 0
    drugs = []
    for x in records:
        if x.drug.drug_category == 'misc':
            drug = {'drug_name': x.drug.drug_name, 'drug_img': x.drug.drug_img}
            drugs.append(drug)
    shelf = [drugs[i:i+3] for i in range(0, len(drugs), 3)]
    if (len(drugs) % 3) > 0:
        partition = len(shelf) - 1
        cabinet['fullshelf'] = shelf[:partition]
        overflow_shelf = shelf[partition:]
        cabinet['overflow'] = overflow_shelf
        overflow = len(overflow_shelf)
    else:
        cabinet['fullshelf'] = shelf
    extra_shelf = 4 - len(shelf)
    
    return render_to_response('info/drugs-misc.html', {'cabinet': cabinet, 'overflow': overflow, 'extra_shelf': extra_shelf}, RequestContext(request))


def allergies_drug_get(request):
    records = UserToAllergy.objects.filter(user=request.user)
    cabinet = {}
    overflow = 0
    allergies = []
    for x in records:
        if x.allergy.allergy_category == 'drug':
            allergy = {'allergy_name': x.allergy.allergy_name, 'allergy_img': x.allergy.allergy_img}
            allergies.append(allergy)
    shelf = [allergies[i:i+3] for i in range(0, len(allergies), 3)]
    if (len(allergies) % 3) > 0:
        partition = len(shelf) - 1
        cabinet['fullshelf'] = shelf[:partition]
        overflow_shelf = shelf[partition:]
        cabinet['overflow'] = overflow_shelf
        overflow = len(overflow_shelf)
    else:
        cabinet['fullshelf'] = shelf
    extra_shelf = 4 - len(shelf)
    
    return render_to_response('info/allergies-drug.html', {'cabinet': cabinet, 'overflow': overflow, 'extra_shelf': extra_shelf}, RequestContext(request))

    
def allergies_diet_get(request):
    records = UserToAllergy.objects.filter(user=request.user)
    cabinet = {}
    overflow = 0
    allergies = []
    for x in records:
        if x.allergy.allergy_category == 'diet':
            allergy = {'allergy_name': x.allergy.allergy_name, 'allergy_img': x.allergy.allergy_img}
            allergies.append(allergy)
    shelf = [allergies[i:i+3] for i in range(0, len(allergies), 3)]
    if (len(allergies) % 3) > 0:
        partition = len(shelf) - 1
        cabinet['fullshelf'] = shelf[:partition]
        overflow_shelf = shelf[partition:]
        cabinet['overflow'] = overflow_shelf
        overflow = len(overflow_shelf)
    else:
        cabinet['fullshelf'] = shelf
    extra_shelf = 4 - len(shelf)
    
    return render_to_response('info/allergies-diet.html', {'cabinet': cabinet, 'overflow': overflow, 'extra_shelf': extra_shelf}, RequestContext(request))

def allergies_misc_get(request):
    records = UserToAllergy.objects.filter(user=request.user)
    cabinet = {}
    overflow = 0
    allergies = []
    for x in records:
        if x.allergy.allergy_category == 'misc':
            allergy = {'allergy_name': x.allergy.allergy_name, 'allergy_img': x.allergy.allergy_img}
            allergies.append(allergy)
    shelf = [allergies[i:i+3] for i in range(0, len(allergies), 3)]
    if (len(allergies) % 3) > 0:
        partition = len(shelf) - 1
        cabinet['fullshelf'] = shelf[:partition]
        overflow_shelf = shelf[partition:]
        cabinet['overflow'] = overflow_shelf
        overflow = len(overflow_shelf)
    else:
        cabinet['fullshelf'] = shelf
    extra_shelf = 4 - len(shelf)
    
    return render_to_response('info/allergies-misc.html', {'cabinet': cabinet, 'overflow': overflow, 'extra_shelf': extra_shelf}, RequestContext(request))
    