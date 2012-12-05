from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, render
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.views.decorators.csrf import csrf_protect

from ergo_info.models import History, FamilyHistory


# USER MEDICAL HISTORY
def user_index(request):
    try:
        condition_entries = History.objects.filter(user=request.user).filter(category=0).order_by('-date')
        accident_entries = History.objects.filter(user=request.user).filter(category=1).order_by('-date')
        surgery_entries = History.objects.filter(user=request.user).filter(category=2).order_by('-date')
        visit_entries = History.objects.filter(user=request.user).filter(category=3).order_by('-date')

        entries = {'condition': condition_entries, 'accident': accident_entries, 'surgery': surgery_entries, 'visit': visit_entries}
        
        no_condition, no_accident, no_surgery, no_visit = False, False, False, False
        if not condition_entries:
            no_condition = True
        if not accident_entries:
            no_accident = True
        if not surgery_entries:
            no_surgery = True
        if not visit_entries:
            no_visit = True
        
        return render_to_response('info/history/user-index.html', {'entries': entries, 'no_condition': no_condition, 'no_accident': no_accident, 'no_surgery': no_surgery, 'no_visit': no_visit}, RequestContext(request))
    
    except:
        pass


def entry_display(request):
    CAT = {
        0: 'Medical Condition',
        1: 'Accident',
        2: 'Surgery',
        3: 'Medical Stay/Visit',
    }
    
    try:
        history_id = request.GET.get('id')
        q = History.objects.get(user=request.user, history_id=history_id)
        entry = {'history_id': q.history_id, 'category': CAT[q.category], 'date': q.date, 'description': q.description}

        return render_to_response('info/history/user-view.html', {'entry': entry}, RequestContext(request))
    except History.DoesNotExist:
        return render(request, 'info/history/user-index.html')
        

def user_add_form(request):
    try:
        return render_to_response('info/history/user-add-dialog.html', RequestContext(request))
    except:
        pass


@csrf_protect
def add_user_history(request):
    try:
        date = request.POST.get('date')
        category = request.POST.get('category')
        description = request.POST.get('description')

        #post_list = [date, category, description]
        #return render_to_response('test.html', {'post_list': post_list}, RequestContext(request))
        
        if date and category and description:
            entry = History(date=date, category=int(category), description=description, user=request.user)
            entry.save()
        else:
            return render(request, 'info/history/user-add-dialog.html', {'error_msg': 'ERROR: Missing information. All fields are required.',})
        
        return HttpResponseRedirect(reverse('ergo_info.views.history.user_index'))
        
    except:
        return render(request, 'info/history/user-add-dialog.html', {'error_msg': 'Error encountered while adding medical history entry. Please try again.',})
        

def user_edit_form(request):
    try:
        history_id = request.GET.get('id')
        date = request.GET.get('date')
        description = request.GET.get('description')
        entry = {'history_id': history_id, 'date': date, 'description': description}

        return render_to_response('info/history/user-edit-dialog.html', {'entry': entry}, RequestContext(request))
    except:
        return render(request, 'info/history/user-view.html', {'error_msg': 'Error encountered while editing medical history entry. Please try again.',})


def edit_user_history(request):
    try:
        history_id = request.POST.get('history_id')
        entry = History.objects.get(user=request.user, history_id=history_id)

        category = request.POST.get('category')
        date = request.POST.get('date')
        description = request.POST.get('description')

        entry.category = category
        entry.date = date
        entry.description = description
        entry.save()

        return HttpResponseRedirect(reverse('ergo_info.views.history.user_index'))
    except History.DoesNotExist:
        return render(request, 'info/history/user-edit-dialog.html', {'error_msg': 'Error encountered while editing medical history entry. Please try again.',})


def remove_user_history(request):
    try:
        history_id = request.POST.get('history_id')
        entry = History.objects.get(user=request.user, history_id=history_id)
        entry.delete()
        
        return HttpResponseRedirect(reverse('ergo_info.views.history.user_index'))
    except History.DoesNotExist:
        return render(request, 'info/history/user-view.html', {'error_msg': 'Error encountered while editing medical history entry. Please try again.',})


    
# FAMILY HISTORY
def family_index(request):
    try:
        entries = FamilyHistory.objects.filter(user=request.user).order_by('-date_added')

        no_entries = False
        if len(entries) < 1:
            no_entries = True
        
        return render_to_response('info/history/family-index.html', {'entries': entries, 'no_entries': no_entries}, RequestContext(request))
    except:
        pass


def family_add_dialog(request):
    try:
        return render_to_response('info/history/family-add-dialog.html', RequestContext(request))
    except:
        pass


def add_family_history(request):
    try:
        rel = request.POST.get('relationship')
        condition = request.POST.get('condition')
        entry = FamilyHistory(relationship=rel, condition=condition, user=request.user)
        entry.save()

        return HttpResponseRedirect(reverse('ergo_info.views.history.family_index'))
    except:
        return render(request, 'info/history/family-add-dialog.html', {'error_msg': 'Error encountered while adding medical history entry. Please try again.',})
        

def family_remove_dialog(request):
    family_id = request.GET.get('id')
    if family_id:
        family_id = int(family_id)
    else:
        family_id = 0
    
    return render_to_response('info/history/family-remove-dialog.html', {'family_id': family_id}, RequestContext(request))
        

def remove_family_history(request):
    try:
        family_id = request.POST.get('family_id')
        entry = FamilyHistory.objects.get(user=request.user, family_id=family_id)
        entry.delete()

        return HttpResponseRedirect(reverse('ergo_info.views.history.family_index'))
    except FamilyHistory.DoesNotExist:
        return render(request, 'info/history/family-remove-dialog.html', {'error_msg': 'Error encountered while removing family emdical history entry. Please try again.',})


    