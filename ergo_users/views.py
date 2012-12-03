from django.shortcuts import render_to_response, render
from django.template import RequestContext
from django.views.decorators.csrf import csrf_protect
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from ergo_users.models import UserProfile


def profile_index(request):
    try:
        profile = UserProfile.objects.filter(user=request.user)[0]
        new_user = False
    except IndexError:
        profile = UserProfile()
        new_user = True
        
    return render_to_response('users/profile.html', {'profile': profile, 'new_user': new_user}, RequestContext(request))


def profile_form(request):
    try:
        profile = UserProfile.objects.filter(user=request.user)[0]
    except IndexError:
        profile = UserProfile()

    return render_to_response('users/profile-edit-form.html', {'profile': profile}, RequestContext(request))
    
    
@csrf_protect
def update_profile(request):
    try:
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
    
        #post_list = [firstname, lastname, dob, sex, email, phone, address, city, state, zipcode]
        #return render_to_response('test.html', {'post_list': post_list}, RequestContext(request))

        if firstname and lastname and dob and sex and email and phone and address and city and state and zipcode:
            request.user.email = email
            request.user.save()
            try:
                profile = UserProfile.objects.filter(user=request.user)[0]
                profile.firstname = firstname
                profile.lastname = lastname
                profile.dob = dob
                profile.sex = sex
                profile.phone = phone
                profile.address = address
                profile.city = city
                profile.state = state
                profile.zipcode = zipcode
                profile.save()
                
            except IndexError:
                new_profile = UserProfile(firstname=firstname, lastname=lastname, dob=dob, sex=sex, phone=phone, address=address, city=city, state=state, zipcode=zipcode, user=request.user)
                new_profile.save()
                
            return HttpResponseRedirect(reverse('ergo_users.views.profile_index'))
        else:
            return render(request, 'users/profile-edit-form.html', {'error_msg': 'Missing Information. All fields are required.',})
            
    except:
        return render(request, 'users/profile-edit-form.html', {'error_msg': 'We are unable to update your profile at this time. Please try again.',})

   