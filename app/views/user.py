from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from app.forms.login import LoginForm
from app.forms.user import UserForm

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
            return HttpResponseRedirect('/account/')

    # if a GET (or any other method) we'll create a blank form
    else:
        if group:
            group = Group.objects.get(name=group)
            form = UserForm(initial={'groups': group})
        else:
            form = UserForm()



    return render(request, 'app/create-account.html', {'form': form})


@login_required
def account(request):
    """Personnal space page view"""

    template = loader.get_template("app/account.html")
    return HttpResponse(template.render(request=request))
