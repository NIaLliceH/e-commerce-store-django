from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.models import User

from .form import CreateUserForm
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