from django.shortcuts import redirect, render, reverse
from django.views.generic import TemplateView


class SignUp(TemplateView):
    template_name = 'registration/signup.html'

def home(request):
    if request.user.is_authenticated:
        if request.user.is_rider:
            return redirect('rider:book')
        elif request.user.is_ex:
            return redirect('exec:alerts')
        else:
            return redirect('logout')
    return render(request, 'rides/home.html')
