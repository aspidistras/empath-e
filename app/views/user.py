"""User related and login required views"""


from django.shortcuts import render, redirect
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.html import format_html
from django.urls import reverse

from app.forms.login import LoginForm
from app.forms.user import UserForm
from app.forms.request import RequestForm
from app.forms.testimony import TestimonyForm

from app.models.request import Request, RequestFilter
from app.models.resources import Disorder
from app.models.testimony import Testimony


# Create your views here.


def user_login(request):
    """Log in page view in order for the user to access his account"""

    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = LoginForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data and authenticate user with processed data
            user = authenticate(username=form.cleaned_data['username'],
                                password=form.cleaned_data['password'])
            if user is not None:
                # a backend authenticated the credentials
                if user.is_active:
                    login(request, user)
                    # redirects to user's account
                    return HttpResponseRedirect('/account/')

            else:
                messages.error(request, 'Le pseudo ou le mot de passe est incorrect.')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = LoginForm()

    return render(request, 'app/login.html', {'form': form})


@login_required
def user_logout(request):
    """Log out user view and redirects to index page"""

    logout(request)
    # redirect to index when user is logged out
    return HttpResponseRedirect('/')


def create_account(request, group=""):
    """Account creating page view"""

    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = UserForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data and create new user with processed data
            user = User.objects.create_user(username=form.cleaned_data['username'],
                                            first_name=form.cleaned_data['first_name'],
                                            last_name=form.cleaned_data['last_name'],
                                            email=form.cleaned_data['email'],
                                            password=form.cleaned_data['password'],
                                            )
            group = Group.objects.get(name=form.cleaned_data['groups'])
            user.groups.add(group)
            user.save()
            form.clean()

            # redirect to a new URL:
            return HttpResponseRedirect('/rules/')

    # if a GET (or any other method) we'll create a blank form
    else:
        if group:
            group = Group.objects.get(name=group)
            form = UserForm(initial={'groups': group})
        else:
            form = UserForm()



    return render(request, 'app/create-account.html', {'form': form})


def rules(request):
    """Thanks for creating an account and community rules page view"""

    template = loader.get_template("app/rules.html")
    return HttpResponse(template.render(request=request))



@login_required
def account(request):
    """Personnal space page view"""

    template = loader.get_template("app/account.html")
    return HttpResponse(template.render(request=request))


@login_required
def delete_account(request):
    """Delete account page view"""

    request.user.delete()
    messages.success(request,
                     "Votre compte et toutes les informations liées ont bien été supprimés.")
    return HttpResponseRedirect('/')


@login_required
def new_request(request):
    """Contact request creating page view"""

    if not request.user.groups.filter(name="Comprendre").exists():
        return redirect('/account/')

    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = RequestForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data and create new Request with processed data
            try:
                disorder = Disorder.objects.get(name=form.cleaned_data['disorders'])
            except:
                disorder = None
            user = request.user
            contact_request = Request.objects.create(message=form.cleaned_data['message'],
                                                     disorder=disorder, user=user)

            contact_request.save()
            form.clean()

            # redirect to a new URL:
            messages.success(request, "Votre requête a bien été prise en compte !")
            return HttpResponseRedirect('/account/')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = RequestForm()


    return render(request, 'app/new-request.html', {'form': form})


@login_required
def new_testimony(request):
    """Testimony creating page view"""

    if not request.user.groups.filter(name="Sensibiliser").exists():
        return redirect('/account/')

    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = TestimonyForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data and create new Request with processed data
            try:
                disorder = Disorder.objects.get(name=form.cleaned_data['disorders'])
            except:
                disorder = None
            user = request.user
            testimony = Testimony.objects.create(content=form.cleaned_data['content'],
                                                 disorder=disorder, user=user)
            testimony.save()
            form.clean()

            # redirect to a new URL:
            messages.success(request, "Merci pour votre témoignage, il a bien été enregistré !")
            return HttpResponseRedirect('/account/')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = TestimonyForm()


    return render(request, 'app/new-testimony.html', {'form': form})


@login_required
def requests_list(request):
    """Requests list page view"""

    if not request.user.groups.filter(name="Sensibiliser").exists():
        return redirect('/account/')

    requests = RequestFilter(request.GET, queryset=Request.objects.filter(status=0))

    return render(request, "app/requests-list.html", {'filter': requests})


@login_required
def request_info(request, request_id):
    """Request accepting info and validation page view"""

    if not request.user.groups.filter(name="Sensibiliser").exists():
        return redirect('/')

    selected_request = Request.objects.get(pk=request_id)

    return render(request, 'app/request-info.html', {'request': selected_request})



@login_required
def accept_request(request, request_id):
    """Request accepting view"""

    if not request.user.groups.filter(name="Sensibiliser").exists():
        return redirect('/')

    selected_request = Request.objects.get(pk=request_id)
    selected_request.status = 1
    selected_request.awareness_user = request.user
    selected_request.save()

    username = selected_request.user.username

    messages.success(request, format_html("Cette requête a bien été acceptée,"
                                          "vous pouvez contactez l'utilisateur "
                                          + username + " en cliquant"
                                          "<a style='color:white;'href='{}'>ici</a>.",
                                          reverse('postman:write', args=[username])))

    return HttpResponseRedirect('/account/')


@login_required
def user_requests_list(request):
    """Displaying accepted requests to both user groups view"""

    if request.user.groups.filter(name="Sensibiliser").exists():
        user_requests = Request.objects.filter(awareness_user=request.user).exclude(status=2)

    elif request.user.groups.filter(name="Comprendre").exists():
        user_requests = Request.objects.filter(user=request.user).filter(status=1)

    else:
        user_requests = []

    return render(request, 'app/user-requests-list.html', {'requests': user_requests})


@login_required
def archive_request(request, request_id):
    """Request archiving view"""

    if not request.user.groups.filter(name="Sensibiliser").exists():
        return redirect('/')

    selected_request = Request.objects.get(pk=request_id)
    selected_request.status = 2
    selected_request.save()

    messages.success(request, "Cette requête a bien été archivée")

    return HttpResponseRedirect('/account/')
