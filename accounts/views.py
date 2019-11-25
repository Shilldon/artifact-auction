from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from accounts.forms import (UserRegistrationForm, UserLoginForm,
                            UserEditProfileForm, ProfileForm)


def register(request):
    """
    Registration
    A view to render the user registration page
    """
    if request.method == "POST":
        registration_form = UserRegistrationForm(request.POST)
        profile_form = ProfileForm()

        if registration_form.is_valid():
            registration_form.save()
            entered_username = registration_form.cleaned_data.get('username')
            entered_password = registration_form.cleaned_data.get('password2')
            user = auth.authenticate(username=entered_username,
                                     password=entered_password)
            """
            Load profile form with instance based on user instance
            """
            profile_form = ProfileForm(request.POST, request.FILES,
                                       instance=user.profile)
            profile_form.save()

            if user:
                messages.success(request,
                                 "You have successfully created an account. "
                                 "Please log in using your credentials.")
                return redirect(reverse('login'))
        elif (registration_form.cleaned_data.get('password2') !=
              registration_form.cleaned_data.get('password1')):
            """
            Provide specific error message for non-matching passwords
            """
            messages.error(request,
                           "Your passwords do not match")
        else:
            """
            All other error messages will be displayed in the form. As the
            form may exceed display height produce generic message at bottom
            of page directing users to review errors on form.
            """
            messages.error(request,
                           "Please check and amend the above.")
    else:
        registration_form = UserRegistrationForm()
        profile_form = ProfileForm()

    return render(request, "register.html", {
                  'registration_form': registration_form,
                  'profile_form': profile_form
                  })


def login(request):
    """
    Login
    check if the user is already logged in and return to index page if so
    otherwise render login form
    """
    if request.user.is_authenticated:
        return redirect(reverse('index'))

    if request.method == "POST":
        login_form = UserLoginForm(request.POST)

        if login_form.is_valid:
            user = auth.authenticate(username=request.POST['username'],
                                     password=request.POST['password'])

        if user:
            """
            Display success message if correctly logged in and go to
            the user's collection page.
            """
            messages.success(request, "Welcome %s." % (user.username))
            auth.login(user=user, request=request)
            return redirect(reverse('view_collection'))
        else:
            """
            Display error message on failure to log in
            """
            messages.error(request, "Your username or password is incorrect")

    else:
        """
        Display login form
        """
        login_form = UserLoginForm()
    return render(request, 'login.html', {"login_form": login_form})

"""
Log out
Ensure user is logged in then provide log out options
"""


@login_required()
def logout(request):
    """
    Clears session collection (items user has won or selected to buy)
    on logging out
    """
    request.session['collection'] = {}
    auth.logout(request)
    messages.success(request, "You have logged out")
    return redirect(reverse('login'))


def view_profile(request, id):
    """
    Profile Page
    Render a user's profile page. It is possible for users who are not
    logged in to view others' profiles.
    """

    user_profile = get_object_or_404(User, pk=id)
    return render(request, "profile.html", {"user_profile": user_profile})


@login_required()
def edit_profile(request):
    """
    Render a form to edit the user's profile but only if user is logged in
    """

    user = request.user

    if request.method == "POST":
        edit_user_form = UserEditProfileForm(request.POST, instance=user)
        edit_profile_form = ProfileForm(request.POST,
                                        request.FILES,
                                        instance=user.profile)

        if edit_user_form.is_valid() and edit_profile_form.is_valid():
            edit_user_form.save()
            edit_profile_form.save()
            return redirect('view_profile', request.user.id)

        else:
            messages.error(request,
                           "Please check and amend the above.")

    else:
        """render user and profile forms"""
        edit_user_form = UserEditProfileForm(instance=user)
        edit_profile_form = ProfileForm(instance=user.profile)

    return render(request, "edit_profile.html",
                  {"edit_user_form": edit_user_form,
                   "edit_profile_form": edit_profile_form
                   }
                  )
