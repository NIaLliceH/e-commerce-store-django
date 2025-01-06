from django.shortcuts import redirect, render
from django.http import HttpResponse
from .form import CreateUserForm

def register(request):
    # making register
    form = CreateUserForm()
    
    # submit the register form
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('store')
    
    data = {
        'form': form
    }

    return render(request, 'account/registration/register.html', context=data)


def email_verification(request):
    pass


def email_verification_sent(request):
    pass


def email_verification_success(request):
    pass


def email_verification_failed(request):
    pass