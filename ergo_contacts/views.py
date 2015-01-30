from django.shortcuts import render_to_response, render
from django.template import RequestContext
from django.views.decorators.csrf import csrf_protect
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from ergo_contacts.models import Contact
from ergo_users.models import UserProfile
from django.core.mail import send_mass_mail
import logging
try:
    from ergo.alert_credentials import *
except ImportError:
    pass


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
        mobile = mobile.replace('-', '').replace('(', '').replace(')', '').replace(' ', '')
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
         
        phone = request.POST.get('mobile')
        phone = phone.replace('-', '').replace('(', '').replace(')', '').replace(' ', '')
        contact.mobile = phone
        
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
            contact = Contact.objects.get(user=request.user, contact_id=contact_id)
            contact.delete()

        return HttpResponseRedirect(reverse('ergo_contacts.views.contacts_index'))
    except Contact.DoesNotExist:
        return render(request, 'contacts/contact-edit-form.html', {'error_msg': 'Error encountered while removing contact. Please try again.',})


def alert_dialog(request):
    return render_to_response('contacts/alert-dialog.html', RequestContext(request))


@csrf_protect
def send_alert(request):
    try: 
        contacts = Contact.objects.filter(user=request.user)

        if not contacts:
            return render_to_response('contacts/alert-status.html', {'status_msg': 'There are no emergency contacts available. Please add your emergency contacts.'}, RequestContext(request))
        else:
            try:
                location = request.POST.get('location', '')
                user = UserProfile.objects.get(user=request.user)
                from_email = request.user.email
                
                msg_list = _build_message_list(user, contacts, location, from_email)

                if len(msg_list) > 0:
                    datatuple = tuple(msg_list)
                    # send alert messages
                    send_mass_mail(datatuple, fail_silently=True, auth_user=ERGO_ALERT_AUTH_USER, auth_password=ERGO_ALERT_AUTH_PASSWORD)
                    
                else:
                    return render_to_response('contacts/alert-status.html', {'status_msg': 'Emergency contact alert options have not been specified. Please edit your emergency contacts.'}, RequestContext(request))

                # return success status
                return render_to_response('contacts/alert-status.html', {'status_msg': 'Emergency contacts have been successfully notified.'}, RequestContext(request))
                    
            except UserProfile.DoesNotExist:
                # return missing profile
                return render_to_response('contacts/alert-status.html', {'status_msg': 'ERROR: Missing user profile.'}, RequestContext(request))

    except:
        return render_to_response('contacts/alert-status.html', {'status_msg': 'Error encountered while alerting emergency contacts. Please try again.'}, RequestContext(request))

        
def _build_message_list(user, contacts, location, from_email):
    subject = 'Medical Emergency Alert Concerning: %s %s' %(user.firstname, user.lastname)
    msg_list = []
            
    for i in contacts:
        message = "Dear %s %s, \n\n%s %s, has been involved in a medical emergency. \n%s is currently being treated at %s. \n\nAs %s's %s, you are listed as one of %s's emergency contacts. This medical emergency alert has been brought to you by ERGO <http://ergo.kennyng.org>.\n" %(i.firstname, i.lastname, user.firstname, user.lastname, user.firstname, location, user.firstname, i.relationship.lower(), user.firstname)

        #print 'MESSAGE: ' + message
        
        recipient_list = _get_recipient_list(i)
        #print 'RECIPIENTS: ' + str(recipient_list)

        if len(recipient_list) > 0:
            msg = (subject, message, from_email, recipient_list)

            #print 'TUPLE: ' + str(msg) 
            
            msg_list.append(msg)

    return msg_list


def _get_recipient_list(contact):
    _GATEWAYS = {
        1: '@txt.att.net',
        2: '@vtext.com',
        3: '@tmomail.net',
        4: '@messaging.sprintpcs.com',
        5: '@vmobl.com',
    }
    
    email_addr, text_addr, fb_addr = None, None, None
    recipient_list = []
    if contact.alert_email:
        recipient_list.append(contact.email)
    if contact.alert_text:
        gateway = _GATEWAYS.get(contact.mobile_carrier, None)
        if gateway:
            text_addr = contact.mobile + gateway
            recipient_list.append(text_addr)
    if contact.alert_fb:
        fb_addr = contact.facebook + '@facebook.com'
        recipient_list.append(fb_addr)

    return recipient_list
