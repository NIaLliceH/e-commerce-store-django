from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


from .form import CreateUserForm, LoginForm, UpdateUserForm
from .token import user_tokenizer_generate

def register(request):
    # making register
    form = CreateUserForm()
    
    # submit the register form
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.is_active = False # deactivate for email verification
            user.save()
            
            current_site = get_current_site(request)
            subject = 'DjangStore account verification'
            message = render_to_string('account/registration/email_verification.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': user_tokenizer_generate.make_token(user)
            })
            
            user.email_user(subject=subject, message=message)
            
            return redirect('email-verification-sent')
    
    data = {
        'form': form
    }

    return render(request, 'account/registration/register.html', context=data)



def email_verification(request, uidb64, token):
    uid = force_str(urlsafe_base64_decode(uidb64))
    user = User.objects.get(pk=uid)
    
    if user and user_tokenizer_generate.check_token(user, token):
        user.is_active = True
        user.save()
        return redirect('email-verification-success')
    else:
        return redirect('email-verification-failed')


def email_verification_sent(request):
    return render(request, 'account/registration/verification_sent.html')


def email_verification_success(request):
    return render(request, 'account/registration/verification_success.html')


def email_verification_failed(request):
    return render(request, 'account/registration/verification_failed.html') 


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        
        if form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')
            
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                login(request, user) # set logged-in status in django
                return redirect('dashboard')
            
    form = LoginForm()
    data = {'form': form}
    return render(request, 'account/user_login.html', context=data)


def user_logout(request):
    logout(request)
    return redirect('store')


@login_required(login_url='user-login')
def dashboard(request):
    return render(request, 'account/dashboard.html')


@login_required(login_url='profile-setting')
def profile_setting(request):
    if request.method == 'POST':
        form = UpdateUserForm(request.POST, instance=request.user)
        
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    
    form = UpdateUserForm(instance=request.user)
    data = {'form': form}
    return render(request, 'account/profile_setting.html', context=data)


@login_required(login_url='delete-account')
def delete_account(request):
    user = User.objects.get(id=request.user.id)
    
    if request.method == 'POST':
        user.delete()
        return redirect('store')
    
    
    return render(request, 'account/delete_account.html')