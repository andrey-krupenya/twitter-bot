from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils.translation import ugettext as _

from app_for_trafic.models import Users, RoleUserTwitter
from ..forms.login import LoginForm


def user_login(request):
    session_keys = list(request.session.keys())

    if 'userid' in session_keys or 'id' in session_keys:
        return HttpResponseRedirect(reverse_lazy('schema-swagger-ui'))

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            try:
                user = Users.objects.filter(
                    email=cd['username'],
                    password=cd['password'],
                    id_role_id=RoleUserTwitter.ADMIN)

                if user.exists():
                    for k, v in user.values()[0].copy().items():
                        request.session[k] = str(v)
                    return HttpResponseRedirect(reverse_lazy('schema-swagger-ui'))

                return HttpResponse(_('Invalid login or password'))
            except Users.DoesNotExist:
                return HttpResponse(_('No such user'))
    else:
        form = LoginForm()
    return render(request, 'registration/login.html', {'form': form})


def user_logout(request):
    request.session.pop("userid", None)
    request.session.pop("id", None)
    request.session.modified = True
    return render(request, 'registration/logged_out.html')
