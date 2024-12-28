from allauth.account.forms import SignupForm
from django.contrib.auth.models import Group
from news_app.models import Puser


class CustomSignupForm(SignupForm):
    def save(self, request):
        user = super().save(request)
        puser = Puser.objects.create(user=user)
        return user
