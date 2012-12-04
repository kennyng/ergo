from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.template import RequestContext


def index(request):
    if request.user.is_authenticated():
        # for authenticated (logged in) users
        return render_to_response('index.html', RequestContext(request))
    else:
        # for anonymous users
        return HttpResponseRedirect('/accounts/login/')


def emergency_access(request):
    return render_to_response('er-access.html', RequestContext(request))

