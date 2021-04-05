from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Avg, Count
from django.forms import inlineformset_factory
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import (CreateView, DeleteView, DetailView, ListView, UpdateView)

from ..decorators import executive_required
from ..forms import ExecutiveSignUpForm
from ..models import User, Ride, Executive, Status

class ExecSignUp(CreateView):
    model = User
    form_class = ExecutiveSignUpForm
    template_name = 'registration/signup_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_type'] = 'executive'
        return context

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('rider:book')

@method_decorator([login_required, executive_required], name='dispatch')
class RideAlert(DetailView):
    model = Ride
    context_object_name = 'alerts'
    template_name = 'rides/executive/ride_alerts.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['rider']
        # context[""]
        return context

@method_decorator([login_required, executive_required], name='dispatch')
class Payments(DetailView):
    pass

@method_decorator([login_required, executive_required], name='dispatch')
class Rides(ListView):
    model = Ride
    
    def get_queryset(self, **kwargs):
        rider = self.request.user.rider
        queryset = Ride.objects.filter(rider=rider)
        return queryset