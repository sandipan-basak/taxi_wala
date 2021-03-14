from django.shortcuts import redirect, render, reverse
from django.views.generic import TemplateView


class SignUp(TemplateView):
    template_name = 'registration/signup.html'


def home(request):
    if request.user.is_authenticated:
        if request.user.is_rider:
            return redirect('rider:book')
        else:
            return redirect('exec:alerts')
    return render(request, 'rides/home.html')
