from django.shortcuts import render, HttpResponse, redirect, reverse, get_object_or_404
from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm
from accounts.forms import UserRegistrationForm, UserLoginForm, UserEditProfileForm

""" render user registration page """
def register(request):
    if request.method == "POST":
        registration_form = UserRegistrationForm(request.POST)
        if registration_form.is_valid():
            registration_form.save()
            entered_username = registration_form.cleaned_data.get('username')
            entered_password = registration_form.cleaned_data.get('password2')
            user = auth.authenticate(username=entered_username, 
                                     password=entered_password)
    
            if user:
                messages.success(request, 
                                 "You have successfully created an account")
                return redirect(reverse('login'))
            else:
                messages.error(request, 
                               "An error occurred, please try again later")
            
    else:
        registration_form = UserRegistrationForm()
    
    return render(request, "register.html", { 
                  "registration_form" : registration_form })

""" check user is logged in or render log in page """
def login(request):
    """check if the user is already logged in and return to index page if so"""
    if request.user.is_authenticated:
        return redirect(reverse('index'))

    """ check the login form posted"""
    if request.method == "POST":
        login_form = UserLoginForm(request.POST)
    
        if login_form.is_valid:
            user = auth.authenticate(username=request.POST['username'],
                                     password=request.POST['password'])
        
        if user:
            #display success message if correctly logged in and return to 
            #index page
            messages.success(request, "You have logged in.")
            auth.login(user=user, request=request)
            return redirect(reverse('index'))
        else:
            login_form.add_error(None,"Your username or password is incorrect")
    
    else:
        #display login form
        login_form = UserLoginForm()    
    return render(request,'login.html', {"login_form" : login_form})

""" Log out """
""" Ensure user is logged in then provide log out options """
@login_required()
def logout(request):
    """Clears collection on logging out"""
    request.session['collection'] = {}
    auth.logout(request)
    messages.success(request, "You have logged out")
    return redirect(reverse('index'))
    
""" Profile Page """
""" Render profile page if the user is logged in """
@login_required()
def view_profile(request):
    return render(request, "profile.html")

""" Render a form to edit the user's profile """
""" Log in check should not be required as link to edit profile is through
    profile page which is not displayed unless logged in"""
@login_required()
def edit_profile(request):
    user = request.user
    
    if request.method == "POST":
        profile_form = UserEditProfileForm(request.POST, instance=user)

        if profile_form.is_valid():
            profile_form.save()
            return redirect('view_profile')
    else:
        profile_form = UserEditProfileForm(instance=user)
    
    return render(request,"edit_profile.html", {"profile_form" : profile_form})