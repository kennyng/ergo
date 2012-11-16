from django.shortcuts import render_to_response
from ergo_users.models import UserProfile
from django.template import RequestContext
from django.views.decorators.csrf import csrf_protect
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

class profile_get(request):
    profile = UserProfile.objects.filter(user=request.user)[0]
    if profile:
        return render_to_response('users/profile.html', {'profile': profile},
                                  context_instance=RequestContext(request))
    else:
        pass
"""    
@csrf_protect
class profile_post(request):
    try:
        current_user = request.user
        profile = UserProfile.objects.filter(user=current_user)[0]
        
        if request.method == 'POST':
            firstname = request.POST.get('firstname')
            lastname = request.POST.get('lastname')
            dob = request.POST.get('dob')
            sex = request.POST.get('sex')
            email = request.POST.get('email')
            phone = request.POST.get('phone')
            address = request.POST.get('address')
            city = request.POST.get('city')
            state = request.POST.get('state')
            zipcode = request.POST.get('zipcode')
        
            if firstname and lastname and dob and sex and phone and address and city and state and zipcode:
                if profile:
                    profile.firstname = firstname
                    profile.lastname = lastname
                    profile.dob = dob
                    profile.sex = sex
                    profile.phone = phone
                    profile.address = address
                    profile.city = address
                    profile.state = state
                    profile.zipcode = zipcode
                    current_user.email = email
                
                    profile.save()
                    current_user.save()
                else:
                    new_profile = UserProfile(firstname=firstname, lastname=lastname, dob=dob, sex=sex, phone=phone, address=address, city=city, state=state, zipcode=zipcode, user=current_user)
                    new_profile.save()
            else:
               
                return HttpResponseRedirect(reverse('/profile#update-profile'), kwargs={'error_msg': 'Missing information. All fields are required.'})
            
            return HttpResponseRedirect(reverse('status/update.html', kwargs={'status_msg': 'Your profile has been successfully updated.', 'return_url': '/profile/', 'button_label': 'Return to Profile'}))
            
    except:
        return HttpResponseRedirect(reverse('/profile#update-profile'), kwargs={'error_msg': 'We are unable to update your profile at this time. Please try again.'})
            
 """