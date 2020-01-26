from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse

from app.models.testimony import Testimony

# Create your views here.


def index(request):
    """Index page view"""

    random_testimony = Testimony.objects.order_by('?').first()

    return render(request, "app/index.html", {'testimony': random_testimony})


def legal_notices(request):
    """Legal notices page view"""

    template = loader.get_template("app/legal-notices.html")
    return HttpResponse(template.render(request=request))


def resources(request):
    """Resources page view"""

    template = loader.get_template("app/resources.html")
    return HttpResponse(template.render(request=request))



def testimonies(request):
    """Testimonies page view"""

    testimonies = Testimony.objects.all()

    return render(request, "app/testimonies.html", {'testimonies': testimonies})

