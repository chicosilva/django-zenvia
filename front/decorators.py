from django.http import HttpResponseRedirect
from functools import wraps
from django.core.urlresolvers import reverse

def verifica_termos_uso():
    def decorator(func):
        def inner_decorator(request, *args, **kwargs):

            from autenticacao.models import Configuracao
            config = Configuracao.objects.all().first()

            if not config.aceitou_termos:
                return HttpResponseRedirect(reverse('autenticacao:termos'))
            else:
                return func(request, *args, **kwargs)

        return wraps(func)(inner_decorator)

    return decorator
