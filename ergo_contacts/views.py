from django.shortcuts import render_to_response, render
from django.template import RequestContext
from django.views.decorators.csrf import csrf_protect
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from ergo_contacts.models import Contact


def contacts_index(request):
    contacts = Contact.objects.filter(user=request.user)
    no_contacts = False
    if not contacts:
        contacts = []
        no_contacts = True
    return render_to_response('contacts/contacts.html', {'contacts': contacts, 'no_contacts': no_contacts}, RequestContext(request))

    
def contacts_add_form(request):
    return render_to_response('contacts/contact-add-form.html', RequestContext(request))

    
@csrf_protect
def add_contact(request):
    try:
        first = request.POST.get('firstname')
        last = request.POST.get('lastname')
        relationship = request.POST.get('relationship')
        email = request.POST.get('email')
        mobile = request.POST.get('mobile')
        fb = request.POST.get('facebook')
        city = request.POST.get('city')
        state = request.POST.get('state')

        carrier_id = request.POST.get('mobile_carrier')
        mobile_carrier = 0;
        if carrier_id:
            mobile_carrier = int(carrier_id)

        alert_options = request.POST.getlist('alert_options')
        alert_email, alert_text, alert_fb = False, False, False
        if 'alert_email' in alert_options:
            alert_email = True
        if 'alert_text' in alert_options:
            alert_text = True
        if 'alert_fb' in alert_options:
            alert_fb = True

        # test POST data
        #post_list = [first, last, relationship, email, mobile, fb, city, state, mobile_carrier, alert_email, alert_text, alert_fb]
        #return render_to_response('test.html', {'post_list': post_list}, RequestContext(request))
        
        new_contact = Contact(firstname=first, lastname=last, relationship=relationship, email=email, mobile=mobile, facebook=fb, city=city, state=state, alert_email=alert_email, alert_text=alert_text, alert_fb=alert_fb, mobile_carrier=mobile_carrier, user=request.user)
        new_contact.save()

        return HttpResponseRedirect(reverse('ergo_contacts.views.contacts_index'))
    except:
        return render(request, 'contacts/contact-add-form.html', {'error_msg': 'Error encountered while adding contact. Please try again.'})
        

def contacts_edit_form(request):
    try:
        contact_id = request.GET.get('id')
        contact = Contact.objects.filter(user=request.user).filter(contact_id=contact_id)[0]
    except:
        pass

    return render_to_response('contacts/contact-edit-form.html', {'contact': contact}, RequestContext(request))


@csrf_protect
def update_contact(request):
    try:
        contact_id = request.GET.get('id')
        contact = Contact.objects.filter(user=request.user).filter(contact_id=contact_id)[0]
        
        # get POST data
        contact.firstname = request.POST.get('firstname')
        contact.lastname = request.POST.get('lastname')
        contact.relationship = request.POST.get('relationship')
        contact.email = request.POST.get('email')
        contact.mobile = request.POST.get('mobile')
        contact.facebook = request.POST.get('facebook')
        contact.city = request.POST.get('city')
        contact.state = request.POST.get('state')
        
        carrier_id = request.POST.get('mobile_carrier')
        mobile_carrier = 0;
        if carrier_id:
            contact.mobile_carrier = int(carrier_id)

        alert_options = request.POST.getlist('alert_options')
        alert_email, alert_text, alert_fb = False, False, False
        if 'alert_email' in alert_options:
            alert_email = True
        if 'alert_text' in alert_options:
            alert_text = True
        if 'alert_fb' in alert_options:
            alert_fb = True
        contact.alert_email = alert_email
        contact.alert_text = alert_text
        contact.alert_fb = alert_fb
        
        contact.save()

        return HttpResponseRedirect(reverse('ergo_contacts.views.contacts_index'))
    except:
        return render(request, 'contacts/contact-edit-form.html', {'error_msg': 'Error encountered while updating contact. Please try again.',})
    

@csrf_protect
def remove_contact(request):
    try:
        contact_id = request.GET.get('id')
        if request.method == 'POST':
            contact = Contact.objects.filter(user=request.user).filter(contact_id=contact_id)[0]
            contact.delete()

        return HttpResponseRedirect(reverse('ergo_contacts.views.contacts_index'))
    except:
        return render(request, 'contacts/contact-edit-form.html', {'error_msg': 'Error encountered while removing contact. Please try again.',})
    