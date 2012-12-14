from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, render
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.views.decorators.csrf import csrf_protect
import json

from ergo_info.models import Immunization, UserToImmunization


def index(request):
    try:
        records = UserToImmunization.objects.filter(user=request.user).order_by('-vaccine_date', '-date_added')
        vaccines = []
        for x in records:
            shot = {'vaccine_id': x.vaccine_id, 'vaccine_name': x.vaccine.vaccine_name, 'vaccine_date': x.vaccine_date}
            vaccines.append(shot)

        no_vaccines = False
        if len(vaccines) < 1:
            no_vaccines = True
        
        return render_to_response('info/immunizations/vaccines.html', {'vaccines': vaccines, 'no_vaccines': no_vaccines}, RequestContext(request))
    except:
        pass
        

def dialog_add(request):
    try:
        vaccines = Immunization.objects.all().order_by('vaccine_name')
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
        return render(request, 'info/immunizations/vaccines-add-dialog.html', {'error_msg': 'Error encountered while adding vaccine. Please try again.',})
        
    
def dialog_remove(request):
    vaccine_id = request.GET.get('id')
    
    return render_to_response('info/immunizations/vaccines-remove-dialog.html', {'vaccine_id': vaccine_id}, RequestContext(request))


@csrf_protect
def remove_vaccine(request):
    try:
        vaccine_id = request.POST.get('vaccine_id')
        if vaccine_id:
            shot = UserToImmunization.objects.get(user=request.user, vaccine_id=vaccine_id)
            shot.delete()
        
        return HttpResponseRedirect(reverse('ergo_info.views.immunizations.index'))
    except Immunization.DoesNotExist:
        return render(request, 'info/immunizations/vaccines-remove-dialog.html', {'error_msg': 'Error encountered while removing vaccine. Please try again.',})


