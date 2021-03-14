from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Avg, Count
from django.forms import inlineformset_factory
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView, TemplateView


from ..decorators import rider_required
from ..forms import RiderSignUpForm, BookRideViewForm
from ..models import Status, User, Ride, Executive, Place

class RiderSignUp(CreateView):
    model = User
    form_class = RiderSignUpForm
    template_name = 'registration/signup_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_type'] = 'rider'
        return context

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('rider:book')

@method_decorator([login_required, rider_required], name='dispatch')
class SetLocation(CreateView):
    
    # form_class = BookRideViewForm
    template_name = 'rides/rider/get_ride.html'
    success_url = reverse_lazy('rider:live')
    
    def form_valid(self, form):
        ride = form.save(commit = False)
        # ride.status = Status.objects.get(name='On Queue')
        ride.save()
        # messages.success(self.request, 'ssup')
        return render('rider:live', ride.pk)

# @method_decorator([login_required, rider_required], name='dispatch')        
# class ConfirmCab(CreateView):
#     model = Ride
    
#     def get_queryset(self, **kwargs):
#         rider = self.request.user.rider
#         queryset = Ride.objects.filter(rider=rider)
        # return queryset

@method_decorator([login_required, rider_required], name='dispatch')
class BookRide(TemplateView):
    pass

@method_decorator([login_required, rider_required], name='dispatch')
class RideStatus(DetailView):
    model = Ride
    context_object_name = 'ride'
    template_name = 'rides/rider/ride_status.html'

    def get_context_data(self, **kwargs):
        kwargs['rider'] = self.get_object().rider
        kwargs['cabee'] = self.get_object().cabee
        return super().get_context_data(**kwargs)



@method_decorator([login_required, rider_required], name='dispatch')
class PastRides(ListView):
    model = Ride
    
    def get_queryset(self, **kwargs):
        rider = self.request.user.rider
        queryset = Ride.objects.filter(rider=rider)
        return queryset


    
