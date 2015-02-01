from django.shortcuts import render_to_response, render
from django.template import RequestContext
from django.views.decorators.csrf import csrf_protect
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.core.files.base import ContentFile
from django.core.files import File
from django.core.files.storage import default_storage as storage

from PIL import Image
import os.path

from ergo_users.models import UserProfile, ProfileImage
from forms import ImageUploadForm


def profile_index(request):
    try:
        profile = UserProfile.objects.get(user=request.user)
        new_user = False
    except UserProfile.DoesNotExist:
        profile = UserProfile()
        new_user = True

    try:
        profile_img = ProfileImage.objects.get(user=request.user)
    except ProfileImage.DoesNotExist:
        profile_img = None

    return render_to_response('users/profile.html', {'profile': profile, 'profile_img': profile_img, 'new_user': new_user}, RequestContext(request))


def profile_form(request):
    try:
        profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        profile = UserProfile()

    return render_to_response('users/profile-edit-form.html', {'profile': profile}, RequestContext(request))


@csrf_protect
def update_profile(request):
    try:
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        dob = request.POST.get('dob')
        sex = request.POST.get('sex')
        blood_type = request.POST.get('blood_type')
        organ_donor = False
        donor = request.POST.get('organ_donor')
        if donor == '1':
            organ_donor = True

        email = request.POST.get('email')
        phone = request.POST.get('phone')
        phone = phone.replace('-', '').replace('(', '').replace(')', '').replace(' ', '')

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
                profile = UserProfile.objects.get(user=request.user)
                profile.firstname = firstname
                profile.lastname = lastname
                profile.dob = dob
                profile.sex = sex
                profile.blood_type = blood_type
                profile.organ_donor = organ_donor
                profile.phone = phone
                profile.address = address
                profile.city = city
                profile.state = state
                profile.zipcode = zipcode
                profile.save()

            except UserProfile.DoesNotExist:
                new_profile = UserProfile(firstname=firstname, lastname=lastname, dob=dob, sex=sex, blood_type=blood_type, organ_donor=organ_donor, phone=phone, address=address, city=city, state=state, zipcode=zipcode, user=request.user)
                new_profile.save()
                
            return HttpResponseRedirect(reverse('ergo_users.views.profile_index'))
        else:
            return render(request, 'users/profile-edit-form.html', {'error_msg': 'Missing Information. All fields are required.',})
            
    except:
        return render(request, 'users/profile-edit-form.html', {'error_msg': 'We are unable to update your profile at this time. Please try again.',})


def offline(request):
    try:
        profile = UserProfile.objects.get(user=request.user)
        new_user = False
    except UserProfile.DoesNotExist:
        profile = UserProfile()
        new_user = True

    return render_to_response('users/offline.html', {'offline': profile, 'new_user': new_user}, RequestContext(request))


@csrf_protect
def upload_profile_image(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            # Save original image to DB and file system to get real path
            uploaded_img = request.FILES.get('image')
            file_content = ContentFile(uploaded_img.read())
            profile_img, created = ProfileImage.objects.get_or_create(user=request.user)
            profile_img.image.save(str(profile_img.id) + '.jpg', file_content)
            profile_img.save()

            # Resize image and save to thumbnail field
            handle_uploaded_image(profile_img)

            # redirect to image upload form with preview after POST
            return HttpResponseRedirect(reverse('ergo_users.views.upload_profile_image'))
    else:
        form = ImageUploadForm() # empty form

    # Load image preview for upload image page
    try:
        profile_img = ProfileImage.objects.get(user=request.user)
    except ProfileImage.DoesNotExist:
        profile_img = None

    return render_to_response('users/upload-image.html', {'profile_img': profile_img, 'form': form}, RequestContext(request))


def handle_uploaded_image(profile_img):
    # Open original image and resize
    # thumb_img = Image.open(profile_img.image.path)
    thumb_img = Image.open(storage.open(profile_img.image.name))
    thumb_img.thumbnail((200, 200), Image.ANTIALIAS)

    # Make temp filename based on model id
    img_name = str(profile_img.id)
    filename = img_name

    # Save thumbnail to temp dir
    temp_img = open(os.path.join('/tmp', filename), 'w')
    thumb_img.save(temp_img, 'JPEG')

    # Read temp file back into a File
    thumb_data = open(os.path.join('/tmp', filename), 'r')
    thumb_file = File(thumb_data)

    profile_img.thumbnail.save(img_name + '.jpg', thumb_file)

