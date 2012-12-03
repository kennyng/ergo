from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, render
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.views.decorators.csrf import csrf_protect

from ergo_info.models import Allergy, UserToAllergy


def _get_allergies_cabinet(request, category):
    records = UserToAllergy.objects.filter(user=request.user)
    cabinet = {}
    overflow = 0
    allergies = []

    # Add all info for allergies to dict for accessing
    for x in records:
        if x.allergy.allergy_category == category:
            allergy = {'allergy_id': x.allergy_id, 'allergy_name': x.allergy.allergy_name, 'allergy_img': x.allergy.allergy_img}
            allergies.append(allergy)

    # Logic for partitioning drugs into full shelves/partial shelves
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

    return cabinet, overflow, extra_shelf
    

def drug_index(request):
    try:
        cabinet, overflow, extra_shelf = _get_allergies_cabinet(request, 'drug')
        return render_to_response('info/allergies/drug.html', {'cabinet': cabinet, 'overflow': overflow, 'extra_shelf': extra_shelf}, RequestContext(request))
    except:
        pass


def diet_index(request):
    try:
        cabinet, overflow, extra_shelf = _get_allergies_cabinet(request, 'diet')
        return render_to_response('info/allergies/diet.html', {'cabinet': cabinet, 'overflow': overflow, 'extra_shelf': extra_shelf}, RequestContext(request))
    except:
        pass


def misc_index(request):
    try:
        cabinet, overflow, extra_shelf = _get_allergies_cabinet(request, 'misc')
        return render_to_response('info/allergies/misc.html', {'cabinet': cabinet, 'overflow': overflow, 'extra_shelf': extra_shelf}, RequestContext(request))
    except:
        pass


def dialog_add(request):
    try:
        allergy_category = request.GET.get('cat')
        allergies = Allergy.objects.filter(allergy_category=allergy_category)
        
        return render_to_response('info/allergies/allergies-add-dialog.html', {'allergy_category': allergy_category, 'allergies': allergies}, RequestContext(request))
    except:
        pass


@csrf_protect
def add_allergy(request):
    _VIEWS = {
        'drug': 'ergo_info.views.allergies.drug_index',
        'diet': 'ergo_info.views.allergies.diet_index',
        'misc': 'ergo_info.views.allergies.misc_index',
    }
    
    try:
        allergy_category = request.POST.get('allergy_category')
        allergy_id = request.POST.get('allergy_id')
        new_allergy = UserToAllergy(user_id=request.user.id, allergy_id=allergy_id)
        new_allergy.save()

        return HttpResponseRedirect(reverse(_VIEWS[allergy_category]))
    except:
        return render(request, 'info/allergies/allergies-add-dialog.html', {'error_msg': 'Error encountered while adding allergy. Please try again.',})


def dialog_remove(request):
    allergy_category = request.GET.get('cat')
    allergy_id = request.GET.get('id')
    if allergy_id:
        allergy_id = int(allergy_id)
    else:
        allergy_id = 0

    return render_to_response('info/allergies/allergies-remove-dialog.html', {'allergy_id': allergy_id, 'allergy_category': allergy_category}, RequestContext(request))


@csrf_protect
def remove_allergy(request):
    _VIEWS = {
        'drug': 'ergo_info.views.allergies.drug_index',
        'diet': 'ergo_info.views.allergies.diet_index',
        'misc': 'ergo_info.views.allergies.misc_index',
    }

    try:
        allergy_category = request.POST.get('allergy_category')
        allergy_id = request.POST.get('allergy_id')
        if allergy_id:
            allergy_id = int(allergy_id)
            allergy = UserToAllergy.objects.filter(user=request.user).filter(allergy_id=allergy_id)[0]
            allergy.delete()

        return HttpResponseRedirect(reverse(_VIEWS[allergy_category]))
    except:
        return render(request, 'info/allergies/allergies-remove-dialog.html', {'error_msg': 'Error encountered while removing allergy. Please try again.',})


# A/B TEST views
def listview_index(request):
    try:
        records = UserToAllergy.objects.filter(user=request.user).order_by('-date_added')
        allergies = []
        for x in records:
            allergy = {'allergy_id': x.allergy_id, 'allergy_name': x.allergy.allergy_name, 'allergy_category': x.allergy.allergy_category, 'allergy_img': x.allergy.allergy_img}
            allergies.append(allergy)

        no_allergies = False
        if len(allergies) < 1:
            no_allergies = True
        
        return render_to_response('info/allergies/listview/index.html', {'allergies': allergies, 'no_allergies': no_allergies}, RequestContext(request))
    except:
        pass


def listview_dialog_add(request):
    try:
        allergies = Allergy.objects.all()
        return render_to_response('info/allergies/listview/add-dialog.html', {'allergies': allergies}, RequestContext(request))
    except:
        pass


@csrf_protect
def listview_add_allergy(request):
    try:
        allergy_id = request.POST.get('allergy_id')
        new_record = UserToAllergy(user_id=request.user.id, allergy_id=allergy_id)
        new_record.save()
        
        return HttpResponseRedirect(reverse('ergo_info.views.allergies.listview_index'))
    except:
        return render(request, 'info/allergies/listview/add-dialog.html', {'error_msg': 'Error encountered while adding allergy. Please try again.',})
        
    
def listview_dialog_remove(request):
    allergy_id = request.GET.get('id')
    if allergy_id:
        allergy_id = int(allergy_id)
    else:
        allergy_id = 0
    
    return render_to_response('info/allergies/listview/remove-dialog.html', {'allergy_id': allergy_id}, RequestContext(request))


@csrf_protect
def listview_remove_allergy(request):
    try:
        allergy_id = request.POST.get('allergy_id')
        if allergy_id:
            allergy_id = int(allergy_id)
            allergy = UserToAllergy.objects.filter(user=request.user).filter(allergy_id=allergy_id)[0]
            allergy.delete()
        
        return HttpResponseRedirect(reverse('ergo_info.views.allergies.listview_index'))
    except:
        return render(request, 'info/allergies/listview/remove-dialog.html', {'error_msg': 'Error encountered while removing allergy. Please try again.',})

        
