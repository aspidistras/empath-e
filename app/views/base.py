from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from django.contrib.auth.models import User

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

    if len(testimonies) > 3:
        # Set paginator with testimonies list and number of testimonies per page
        paginator = Paginator(testimonies, 3)
        page = request.GET.get('page')
        try:
            testimonies = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            testimonies = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            testimonies = paginator.page(paginator.num_pages)

        is_paginated = True
    else:
        is_paginated = False

    return render(request, "app/testimonies.html", {'testimonies': testimonies, 'paginate': is_paginated})
