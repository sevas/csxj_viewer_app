from django.http import HttpResponse
from django.template import Context, loader

def index(request):

    return HttpResponse(request.path)


def archives(request):
    t = loader.get_template('provider_main.html')

    return HttpResponse(t.render({}))
