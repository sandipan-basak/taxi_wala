from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Avg, Count
from django.forms import inlineformset_factory
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import (CreateView, DeleteView, DetailView, ListView, UpdateView, TemplateView)
from django.views.generic.edit import FormMixin
from django.urls import reverse_lazy
from ..decorators import executive_required
from ..forms import ExecutiveSignUpForm
from ..models import User, Ride, Executive, Status

from rides.utils.google_api_util import GoogleApiHandler
from rides.utils.random_locations import Location_Generator

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
        return redirect('exec:alerts')

@method_decorator([login_required, executive_required], name='dispatch')
class RideAlert(UpdateView):
    model = Executive
    fields = '__all__'
    template_name = 'rides/exec/ride_alerts.html'

    def get_object(self):
        return self.request.user.executive

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        partner = self.get_object()
        print(partner.user.name)
        st = Status.objects.get(name="On Queue")
        curr_ride = partner.ride_set.all().filter(status=st).first()
        context["curr_position"] = [partner.car.lat, partner.car.lng]
        if not curr_ride:
            context['ride_available'] = False
        else:
            context['ride_available'] = True
            context['ride'] = curr_ride
            print(context['ride'].rider.name)
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(**kwargs)
        partner = self.get_object()
        on = Status.objects.get(name="Ongoing")
        curr_ride = context['ride']
        if 'c_ride' in request.POST:
            print("cancels ride")
            curr_ride.cabee = None
            curr_ride.save()
            return redirect('exec:alerts')
        elif 'a_ride' in request.POST:
            partner.is_engaged = True
            partner.save()
            curr_ride.status = on
            curr_ride.save()
            return redirect('exec:maps')        
        return render(request, self.template_name, context=context)    

@method_decorator([login_required, executive_required], name='dispatch')
class Maps(UpdateView):
    model = Executive
    fields = '__all__'
    template_name = 'rides/exec/map_view.html'
    gL = Location_Generator()
    gAPI = GoogleApiHandler()
    
    def get_object(self):
        return self.request.user.executive

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        partner = self.get_object()
        print(partner.user.username)
        status = Status.objects.get(name="Ongoing")
        context['ride_available'] = False if not partner.is_engaged else True
        print(context['ride_available'])
        context['curr_position'] = [partner.car.lat, partner.car.lng]
        if context['ride_available']:
            ride = partner.ride_set.filter(status=status).first()
            context['ride'] = ride
            context['source'] = self.gL.get_coor(ride.source)
            print(context['source'])
            context['dest'] = self.gL.get_coor(ride.destination)
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        partner = self.get_object()
        context = self.get_context_data(**kwargs)
        if context['ride_available']:
            curr_ride = context['ride']
            complete = Status.objects.get(name="Completed")
            cancel = Status.objects.get(name="Cancelled")            
            if request.method == 'POST':
                if 'c_ride' in request.POST:
                    curr_ride.cabee = None
                    curr_ride.cab = None
                    curr_ride.status = cancel
                    curr_ride.save()
                    partner.is_engaged = False
                    partner.save()
                    context['ride_available'] = False
                elif 's_ride' in request.POST:
                    curr_ride.is_started = True
                    curr_ride.save()
                    cab_reached = self.gAPI.get_nearest_road(self.gL.get_coor(curr_ride.source))
                    partner.car.lat = cab_reached[0]
                    partner.car.lng = cab_reached[1]
                    partner.car.save()
                    context['curr_position'] = [partner.car.lat, partner.car.lng]
                elif 'f_ride' in request.POST:
                    curr_ride.is_started = False
                    curr_ride.status = complete
                    curr_ride.save()
                    partner.is_engaged = False
                    partner.save()
                    context['ride_available'] = False
        return render(request, self.template_name, context=context)

@method_decorator([login_required, executive_required], name='dispatch')
class Payments(TemplateView):
    template_name = 'rides/exec/payments.html'

@method_decorator([login_required, executive_required], name='dispatch')
class PastRides(ListView):
    model = Ride
    context_object_name = "rides"
    template_name = 'rides/exec/ride_history.html'
    # queryset = Ride.objects.exclude(status=Status.objects.get(name="On Queue"))

    def get_queryset(self):
        queryset = Ride.objects.exclude(status=Status.objects.get(name="On Queue")).filter(cabee=self.request.user.executive)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        rides = Ride.objects.exclude(status=Status.objects.get(name="On Queue")).filter(cabee=self.request.user.executive)
        print(rides.count())
        context['ride_available'] = False if rides.count() == 0 else True
        return context
