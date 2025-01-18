from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect

from django.utils import timezone
import pytz

from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect


@csrf_protect
def change_timezone(request):
    if request.method == 'POST':
        request.session['django_timezone'] = request.POST['timezone']
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))