from django.shortcuts import render

# SIGN-UP / REGISTER
def sign_up(request):
    return render(request, 'registration/registration.html')


# SIGN-IN / LOG IN
def sign_in(request):
    pass


# SIGN-OUT / LOG OUT
def sign_out(request):
    pass