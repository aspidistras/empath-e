from django.template import loader
from django.http import HttpResponse

# Create your views here.


def index(request):
    """Index page view"""

    template = loader.get_template("app/index.html")
    return HttpResponse(template.render(request=request))


def legal_notices(request):
    """Legal notices page view"""

    template = loader.get_template("app/legal-notices.html")
    return HttpResponse(template.render(request=request))


def resources(request):
    """Resources page view"""

    template = loader.get_template("app/resources.html")
    return HttpResponse(template.render(request=request))
