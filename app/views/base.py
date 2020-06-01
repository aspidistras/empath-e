"""Basic app views"""


from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.core.mail import send_mail
from django.contrib import messages

from app.models.testimony import Testimony
from app.models.resources import Disorder, Link
from app.forms.contact import ContactForm

# Create your views here.


def index(request):
    """Index page view"""

    random_testimony = Testimony.objects.order_by('?').first()

    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = ContactForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data and authenticate user with processed data
            subject = form.cleaned_data['subject']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']
            try:
                send_mail(subject,
                          "Message suivant : '" + message + "' de la part de " + email,
                          email, ['empath.e.oc@gmail.com'])
                messages.success(request, 'Votre message a bien été envoyé !')
            except:
                messages.error(request,
                               'Le formulaire de contact n\' pas pu être soumis,'
                               'veuillez réessayer plus tard.')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = ContactForm()


    return render(request, "app/index.html", {'form': form, 'testimony': random_testimony})


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


def about(request):
    """About project page view"""

    template = loader.get_template("app/about.html")
    return HttpResponse(template.render(request=request))


def disorders_list(request):
    """Disorders list page view"""
    disorders = Disorder.objects.all()

    return render(request, "app/disorders.html", {'disorders': disorders})


def disorder_details(request, disorder_name):
    """Disoders details and resources page view"""

    disorder = Disorder.objects.get(url_pattern=disorder_name)
    links = Link.objects.filter(disorder=disorder)

    return render(request, "app/disorder-details.html", {'disorder': disorder, 'links': links})
