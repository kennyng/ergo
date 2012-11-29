from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.views.decorators.csrf import csrf_protect
import json

from ergo_info.models import Immunization, UserToImmunization


def index(request):
    records = UserToImmunization.objects.filter(user=request.user).order_by('-vaccine_date', '-date_added')
    vaccines = []
    for x in records:
        shot = {'vaccine_id': x.vaccine_id, 'vaccine_name': x.vaccine.vaccine_name, 'vaccine_date': x.vaccine_date}
        vaccines.append(shot)

    new_user = False
    if len(vaccines) < 1:
        new_user = True
        
    return render_to_response('info/immunizations/vaccines.html', {'vaccines': vaccines, 'new_user': new_user}, RequestContext(request))


def dialog_add(request):
    try:
        vaccines = Immunization.objects.all()
        return render_to_response('info/immunizations/vaccines-add-dialog.html', {'vaccines': vaccines}, RequestContext(request))
    except:
        pass


@csrf_protect
def add_vaccine(request):
    try:
        vaccine_id = request.POST.get('vaccine_id')
        vaccine_date = request.POST.get('vaccine_date')
        new_record = UserToImmunization(user_id=request.user.id, vaccine_id=vaccine_id, vaccine_date=vaccine_date)
        new_record.save()
        
        return HttpResponseRedirect(reverse('ergo_info.views.immunizations.index'))
    except:
        return(request, 'info/immunizations/vaccines-add-dialog.html', {'error_msg': 'Error encountered while adding vaccine. Please try again.'})
        
    
def dialog_remove(request):
    vaccine_id = request.GET.get('id')
    if vaccine_id:
        vaccine_id = int(vaccine_id)
    else:
        vaccine_id = 0
    
    return render_to_response('info/immunizations/vaccines-remove-dialog.html', {'vaccine_id': vaccine_id}, RequestContext(request))


@csrf_protect
def remove_vaccine(request):
    try:
        vaccine_id = request.GET.get('id')
        if vaccine_id and request.method == 'POST':
            vaccine_id = int(vaccine_id)
            shot = UserToImmunization.objects.filter(user=request.user).filter(vaccine_id=vaccine_id)[0]
            shot.delete()
        
        return HttpResponseRedirect(reverse('ergo_info.views.immunizations.index'))
    except:
        render(request, 'info/immunizations/vaccines-remove-dialog.html', {'error_msg': 'Error encountered while removing vaccine. Please try again.',})


