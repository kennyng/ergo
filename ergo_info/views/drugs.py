from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, render
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.views.decorators.csrf import csrf_protect

from ergo_info.models import Drug, UserToDrug


def _get_drugs_cabinet(request, category):
    records = UserToDrug.objects.filter(user=request.user).filter(category=category)
    drugs = []

    # Add all info for drugs to dict for accessing
    for x in records:
        drug = {'drug_id': x.drug_id, 'drug_name': x.drug.name, 'drug_img': x.drug.image}
        drugs.append(drug)

    cabinet = {'one': [], 'two': [], 'three': []}
    extra_shelf = 4
    no_drugs, one_drug, two_drug = False, False, False
    if len(drugs) == 0:
        no_drugs = True
    elif len(drugs) == 1:
        cabinet['one'] = drugs
        extra_shelf = 3
        one_drug = True
    elif len(drugs) == 2:
        cabinet['two'] = drugs
        extra_shelf = 3
        two_drug = True
    elif len(drugs) == 3:
        cabinet['three'] = [drugs]
        extra_shelf = 3
    elif len(drugs) > 3:
        # Logic for partitioning drugs into full shelves/partial shelves
        shelf = [drugs[i:i+3] for i in range(0, len(drugs), 3)]

        if (len(drugs) % 3) > 0:
            partition = len(shelf) - 1
            cabinet['three'] = shelf[:partition]
            overflow_drugs = shelf[partition:][0]
            if len(overflow_drugs) == 1:
                cabinet['one'] = overflow_drugs
                one_drug = True
            elif len(overflow_drugs) == 2:
                cabinet['two'] = overflow_drugs
                two_drug = True
        else:
            cabinet['three'] = shelf
        extra_shelf = 4 - len(shelf)

    return cabinet, extra_shelf, no_drugs, one_drug, two_drug
    

def prescription_index(request):
    try:
        cabinet, extra_shelf, no_drugs, one_drug, two_drug = _get_drugs_cabinet(request, 0)
        return render_to_response('info/drugs/prescription.html', {'cabinet': cabinet, 'extra_shelf': extra_shelf, 'no_drugs': no_drugs, 'one_drug': one_drug, 'two_drug': two_drug}, RequestContext(request))
    except:
        pass


def otc_index(request):
    try:
        cabinet, extra_shelf, no_drugs, one_drug, two_drug = _get_drugs_cabinet(request, 1)
        return render_to_response('info/drugs/otc.html', {'cabinet': cabinet, 'extra_shelf': extra_shelf, 'no_drugs': no_drugs, 'one_drug': one_drug, 'two_drug': two_drug}, RequestContext(request))
    except:
        pass


def misc_index(request):
    try:
        cabinet, extra_shelf, no_drugs, one_drug, two_drug = _get_drugs_cabinet(request, 2)
        return render_to_response('info/drugs/misc.html', {'cabinet': cabinet, 'extra_shelf': extra_shelf, 'no_drugs': no_drugs, 'one_drug': one_drug, 'two_drug': two_drug}, RequestContext(request))
    except:
        pass


def dialog_add(request):
    try:
        drug_category = request.GET.get('cat')
        drugs = Drug.objects.filter(category=drug_category)
        
        return render_to_response('info/drugs/drugs-add-dialog.html', {'drug_category': drug_category, 'drugs': drugs}, RequestContext(request))
    except:
        pass


@csrf_protect
def add_drug(request):
    _VIEWS = {
        '0': 'ergo_info.views.drugs.prescription_index',
        '1': 'ergo_info.views.drugs.otc_index',
        '2': 'ergo_info.views.drugs.misc_index',
    }
    
    try:
        drug_category = request.POST.get('drug_category')
        drug_id = request.POST.get('drug_id')
        new_drug = UserToDrug(user_id=request.user.id, drug_id=drug_id, category=drug_category)
        new_drug.save()

        return HttpResponseRedirect(reverse(_VIEWS[drug_category]))
    except:
        return render(request, 'info/drugs/drugs-add-dialog.html', {'error_msg': 'Error encountered while adding drug. Please try again.',})


def dialog_remove(request):
    drug_category = request.GET.get('cat')
    drug_id = request.GET.get('id')

    return render_to_response('info/drugs/drugs-remove-dialog.html', {'drug_id': drug_id, 'drug_category': drug_category}, RequestContext(request))


@csrf_protect
def remove_drug(request):
    _VIEWS = {
        '0': 'ergo_info.views.drugs.prescription_index',
        '1': 'ergo_info.views.drugs.otc_index',
        '2': 'ergo_info.views.drugs.misc_index',
    }

    try:
        drug_category = request.POST.get('drug_category')
        drug_id = request.POST.get('drug_id')
        if drug_id:
            drug = UserToDrug.objects.get(user=request.user, drug_id=drug_id)
            drug.delete()

        return HttpResponseRedirect(reverse(_VIEWS[drug_category]))
    except UserToDrug.DoesNotExist:
        return render(request, 'info/drugs/drugs-remove-dialog.html', {'error_msg': 'Error encountered while removing drug. Please try again.',})

