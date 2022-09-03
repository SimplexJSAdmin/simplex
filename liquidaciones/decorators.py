from django.shortcuts import redirect, render
from django.contrib import messages
from .models import Empresa


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
                        if( 'id_empresa' not in request.session.keys()):
                            messages.error(request, 'Primero debe seleccionar la empresa antes de trabajar con los modulos')
                            return redirect('inicio')
                        empresa_sesion = Empresa.objects.get(id_empresa = request.session['id_empresa'])
                        messages.info(request, 'Usted esta trabajando para la empresa, {}'.format(empresa_sesion.nombre_empresa))
                        return view_func(request, *args, **kwargs)
                    else:
                        continue
                else:
                    return redirect('inicio')
            else:
                return redirect('inicio')
        return wrapper_func
    return decorator