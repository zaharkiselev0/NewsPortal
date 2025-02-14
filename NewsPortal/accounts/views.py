from django.shortcuts import render
from django.template.response import TemplateResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from .models import Subscriptions
from news_app.models import Puser
from django.http import HttpResponseRedirect
from django.views.generic import DetailView
import pytz
from django.utils import timezone


@login_required
@csrf_protect
def subscribe(request):
    if request.method == 'POST':
        action = request.POST.get('action')
        sub_pk = request.POST.get('sub_pk')
        sub = Puser(pk=sub_pk)
        follower = Puser(user=request.user)
        if action == 'subscribe':
            Subscriptions.objects.create(follower=follower, sub=sub)
        elif action == 'unsubscribe':
            Subscriptions.objects.filter(follower=follower, sub=sub).delete()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def profile(request):
    puser = request.user.puser
    posts = puser.post_set.all()
    subs = Puser.objects.filter(subs__follower=puser)
    return TemplateResponse(request, 'accounts/profile.html',
                            context={'puser': puser, 'posts': posts, 'subs': subs,
                                     'timezones': pytz.common_timezones,
                                     'current_time': timezone.localtime(timezone.now())})


change_attributes = ['description', 'send_mail']
@login_required
@csrf_protect
def change_user_info(request):
    if request.method == 'POST':
        puser = request.user.puser
        for attr_name in change_attributes:
            if attr_name in request.POST:
                puser.__setattr__(attr_name, request.POST.get(attr_name))
        puser.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class UserDetail(DetailView):
    model = Puser
    template_name = 'accounts/puser.html'
    context_object_name = 'puser'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            puser = self.request.user.puser
            sub_pk = self.get_object().pk
            subscribed = puser.subscriptions.filter(pk=sub_pk).exists()
            context['subscribed'] = subscribed
            context['sub_pk'] = sub_pk
        return context
