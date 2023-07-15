from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import IntegrityError
from .forms import CreateUserForm


# view for rendering homepage
def home(request):
    return render(request, "account/home.html")


# view for rendering signup page
def signupuser(request):
    if request.user.is_authenticated:
        return redirect('/')
    if request.method == 'GET':
        return render(request, 'account/signup.html', {'form': CreateUserForm()})
    else:
        if len(request.POST['username']) > 15:
            messages.error(request, " Username must be max 15 characters, Please try again")
            return render(request, 'account/signup.html', {'form': CreateUserForm()})
        if not request.POST['username'].isalnum():
            messages.error(request, "Username should only contain letters and numbers, Please try again")
            return render(request, 'account/signup.html', {'form': CreateUserForm()})
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(request.POST['username'], password=request.POST['password1'],
                                                first_name=request.POST['first_name'],
                                                last_name=request.POST['last_name'])
                user.save()
                login(request, user)
                return redirect('/')
            except IntegrityError:
                messages.error(request, "Username already taken, Please try something else!")
                return render(request, 'account/signup.html', {'form': CreateUserForm()})
        else:
            messages.error(request, "Passwords did not match, Please try something else!")
            return render(request, 'account/signup.html', {'form': CreateUserForm()})


def loginuser(request):
    if request.user.is_authenticated:
        return redirect('/')
    if request.method == 'GET':
        return render(request, "account/login.html")
    if request.method == "POST":
        user_name = request.POST.get('name', '')
        user_password = request.POST.get('password', '')

        user = authenticate(username=user_name, password=user_password)

        if user is not None:
            login(request, user)
            messages.success(request, " Successfully logged in")
            return redirect('/')
        else:
            messages.error(request, " Invalid Credentials, Please try again")
            return render(request, 'account/home.html')


# view for rendering logout
@login_required
def handlelogout(request):
    logout(request)
    messages.success(request, " Successfully logged out")
    return redirect('/')


# view for rendering change password
class ChangePassword(LoginRequiredMixin, TemplateView):
    template_name = "account/passwordchange.html"

    def post(self, request):
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, user=request.user)
            messages.success(request, "Changed Password successfully")
            return redirect('/')
        else:
            for err in form.errors.values():
                messages.error(request, err)
            return redirect('/changepass')

    def get(self, request):
        form = PasswordChangeForm(user=request.user)
        return render(request, self.template_name, {"form": form})
