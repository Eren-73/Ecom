from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from .forms import VendorSignUpForm, CustomerSignUpForm, VendorProfileForm, CustomerProfileForm

# -------------------
# Signup
# -------------------
def vendor_signup(request):
    if request.method == 'POST':
        user_form = VendorSignUpForm(request.POST)
        profile_form = VendorProfileForm(request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save(commit=False)
            user.set_password(user_form.cleaned_data['password'])
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            login(request, user)
            return redirect('dashboard_vendor')
    else:
        user_form = VendorSignUpForm()
        profile_form = VendorProfileForm()
    return render(request, 'accounts/vendor_signup.html', {'user_form': user_form, 'profile_form': profile_form})


def customer_signup(request):
    if request.method == 'POST':
        user_form = CustomerSignUpForm(request.POST)
        profile_form = CustomerProfileForm(request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save(commit=False)
            user.set_password(user_form.cleaned_data['password'])
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            login(request, user)
            return redirect('dashboard_customer')
    else:
        user_form = CustomerSignUpForm()
        profile_form = CustomerProfileForm()
    return render(request, 'accounts/customer_signup.html', {'user_form': user_form, 'profile_form': profile_form})


# -------------------
# Login / Logout
# -------------------
def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            # Redirection selon rôle
            if hasattr(user, 'vendor_profile'):
                return redirect('dashboard_vendor')
            elif hasattr(user, 'customer_profile'):
                return redirect('dashboard_customer')
            else:
                messages.error(request, "Profil introuvable.")
                logout(request)
                return redirect('login')
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})


@login_required
def logout_view(request):
    logout(request)
    return redirect('home')


# -------------------
# Dashboards
# -------------------
@login_required
def dashboard_vendor(request):
    return render(request, 'accounts/dashboard_vendor.html')


@login_required
def dashboard_customer(request):
    return render(request, 'accounts/dashboard_customer.html')
