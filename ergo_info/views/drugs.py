from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, render
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.views.decorators.csrf import csrf_protect

from ergo_info.models import Drug, UserToDrug


def _get_drugs_cabinet(request, category):
    records = UserToDrug.objects.filter(user=request.user)
    cabinet = {}
    overflow = 0
    drugs = []

    # Add all info for drugs to dict for accessing
    for x in records:
        if x.drug.drug_category == category:
            drug = {'drug_id': x.drug_id, 'drug_name': x.drug.drug_name, 'drug_img': x.drug.drug_img}
            drugs.append(drug)

    # Logic for partitioning drugs into full shelves/partial shelves
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

    return cabinet, overflow, extra_shelf
    

def otc_index(request):
    try:
        cabinet, overflow, extra_shelf = _get_drugs_cabinet(request, 'otc')
        return render_to_response('info/drugs/otc.html', {'cabinet': cabinet, 'overflow': overflow, 'extra_shelf': extra_shelf}, RequestContext(request))
    except:
        pass


def prescription_index(request):
    try:
        cabinet, overflow, extra_shelf = _get_drugs_cabinet(request, 'prescription')
        return render_to_response('info/drugs/prescription.html', {'cabinet': cabinet, 'overflow': overflow, 'extra_shelf': extra_shelf}, RequestContext(request))
    except:
        pass


def misc_index(request):
    try:
        cabinet, overflow, extra_shelf = _get_drugs_cabinet(request, 'misc')
        return render_to_response('info/drugs/misc.html', {'cabinet': cabinet, 'overflow': overflow, 'extra_shelf': extra_shelf}, RequestContext(request))
    except:
        pass


def dialog_add(request):
    try:
        drug_category = request.GET.get('cat')
        drugs = Drug.objects.filter(drug_category=drug_category)
        
        return render_to_response('info/drugs/drugs-add-dialog.html', {'drug_category': drug_category, 'drugs': drugs}, RequestContext(request))
    except:
        pass


@csrf_protect
def add_drug(request):
    _VIEWS = {
        'prescription': 'ergo_info.views.drugs.prescription_index',
        'otc': 'ergo_info.views.drugs.otc_index',
        'misc': 'ergo_info.views.drugs.misc_index',
    }
    
    try:
        drug_category = request.POST.get('drug_category')
        drug_id = request.POST.get('drug_id')
        new_drug = UserToDrug(user_id=request.user.id, drug_id=drug_id)
        new_drug.save()

        return HttpResponseRedirect(reverse(_VIEWS[drug_category]))
    except:
        return render(request, 'info/drugs/drugs-add-dialog.html', {'error_msg': 'Error encountered while adding drug. Please try again.',})


def dialog_remove(request):
    drug_category = request.GET.get('cat')
    drug_id = request.GET.get('id')
    if drug_id:
        drug_id = int(drug_id)
    else:
        drug_id = 0

    return render_to_response('info/drugs/drugs-remove-dialog.html', {'drug_id': drug_id, 'drug_category': drug_category}, RequestContext(request))


@csrf_protect
def remove_drug(request):
    _VIEWS = {
        'prescription': 'ergo_info.views.drugs.prescription_index',
        'otc': 'ergo_info.views.drugs.otc_index',
        'misc': 'ergo_info.views.drugs.misc_index',
    }

    try:
        drug_category = request.POST.get('drug_category')
        drug_id = request.POST.get('drug_id')
        if drug_id:
            drug_id = int(drug_id)
            drug = UserToDrug.objects.filter(user=request.user).filter(drug_id=drug_id)[0]
            drug.delete()

        return HttpResponseRedirect(reverse(_VIEWS[drug_category]))
    except:
        return render(request, 'info/drugs/drugs-remove-dialog.html', {'error_msg': 'Error encountered while removing drug. Please try again.',})

