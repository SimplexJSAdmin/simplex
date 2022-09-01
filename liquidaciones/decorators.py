from django.shortcuts import redirect, render

def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('inicio')
        else:
            return view_func(request, *args, **kwargs)
    return wrapper_func

def allowed_users(alloweds=[]):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):
            group = None
            if request.user.groups.exists():
                group_name = [*map(lambda x: x.name, request.user.groups.all())]
                for group_allowed in alloweds:
                    if group_allowed in group_name:
                        return view_func(request, *args, **kwargs)
                    else:
                        continue
                else:
                    return redirect('inicio')
            else:
                return redirect('inicio')
        return wrapper_func
    return decorator