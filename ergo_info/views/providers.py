from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.views.decorators.csrf import csrf_protect

from ergo_info.models import Provider


def index(request):
    try:
        provider = Provider.objects.filter(user=request.user)[0]
        new_user = False
    except IndexError:
        provider = Provider()
        new_user = True
        
    return render_to_response('info/providers/providers.html', {'provider': provider, 'new_user': new_user}, RequestContext(request))


def edit_form(request):
    try:
        provider = Provider.objects.filter(user=request.user)[0]
    except IndexError:
        provider = Provider()

    return render_to_response('info/providers/providers-edit-form.html', {'provider': provider}, RequestContext(request))


@csrf_protect
def edit_providers(request):
    try:
        insurance_name = request.POST.get('insurance_name')
        group_num = request.POST.get('group_num')
        policy_num = request.POST.get('policy_num')
        insurance_contact = request.POST.get('insurance_contact')
        pcp_name = request.POST.get('pcp_name')
        pcp_contact = request.POST.get('pcp_contact')
        pcp_location = request.POST.get('pcp_location')
        pcp_address = request.POST.get('pcp_address')
        pcp_city = request.POST.get('pcp_city')
        pcp_state = request.POST.get('pcp_state')
        pcp_zipcode = request.POST.get('pcp_zipcode')

        # test POST data
        #post_list = [insurance_name, group_num, policy_num, insurance_contact, pcp_name, pcp_contact, pcp_location, pcp_address, pcp_city, pcp_state, pcp_zipcode]
        #return render_to_response('test.html', {'post_list': post_list}, RequestContext(request))

        try:
            provider = Provider.objects.filter(user=request.user)[0]

            provider.insurance_name = insurance_name
            provider.group_num = group_num
            provider.policy_num = policy_num
            provider.insurance_contact = insurance_contact
            provider.pcp_name = pcp_name
            provider.pcp_contact = pcp_contact
            provider.pcp_location = pcp_location
            provider.pcp_address = pcp_address
            provider.pcp_city = pcp_city
            provider.pcp_state = pcp_state
            provider.pcp_zipcode = pcp_zipcode

            provider.save()
        except IndexError:
            new_provider = Provider(insurance_name=insurance_name, group_num=group_num, policy_num=policy_num, insurance_contact=insurance_contact, pcp_name=pcp_name, pcp_contact=pcp_contact, pcp_location=pcp_location, pcp_address=pcp_address, pcp_city=pcp_city, pcp_state=pcp_state, pcp_zipcode=pcp_zipcode, user=request.user)
            new_provider.save()

        return HttpResponseRedirect(reverse('ergo_info.views.providers.index'))
    except:
        return render(request, 'users/providers-edit-form.html', {'error_msg': 'We are unable to update your providers at this time. Please try again.',})

