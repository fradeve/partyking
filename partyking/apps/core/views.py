__appname__ = "PartyKing"
__author__  = "Francesco de Virgilio (fradeve)"
__license__ = "GNU GPL 3.0 or later"

__version__ = "0.1"

from partyking.apps.core.models import Profile
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.template import RequestContext

def chart(request):
    profiles = Profile.objects.order_by('-rating')
    return render_to_response('chart.html', {'profiles': profiles})

@login_required(login_url='/login/')
def vote(request):
    profiles = Profile.objects.order_by('-lastname')
    return render_to_response('userpage.html',
                              {'profiles': profiles},
                              context_instance=RequestContext(request))

#TODO:  csrf middleware is currently deactivated, you must re-enable it
#       and find out what's wrong
def addvote(request):
    if request.is_ajax():
        if request.method == ('GET'):
            print('running GET instance')
            loggeduser = request.user.get_profile()
            if loggeduser.voted < 3:
                loggeduser.voted += 1
                loggeduser.save()
                return HttpResponse('proceed')
            else:
                return HttpResponse()
        if request.method == ('POST'):
            print('running POST instance')
            activeuser = Profile.objects.get(fbid=request.POST.get('user'))
            if request.POST.get('action') == 'rmvote':
                activeuser.rating -= 1
            else:
                activeuser.rating += 1
            activeuser.save()
            return HttpResponse()

def logout_view(request, next_page='/'):
    logout(request)