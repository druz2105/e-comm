from django.http import HttpResponse
from django.shortcuts import redirect


def authenticate_user(view_func):
    def wrap(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('/home/')
        else:
            return view_func(request, *args, **kwargs)

    return wrap


def allowed_user(allowed_roles=[]):
    def deco(view_func):
        def wrap(request, *args, **kwargs):
            group = None
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name
            if group in allowed_roles:
                return view_func(request, *args, **kwargs)
            else:
                return HttpResponse('You Are Not Authorized')
        return wrap

    return deco
