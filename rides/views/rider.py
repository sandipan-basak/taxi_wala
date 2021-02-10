from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Avg, Count
from django.forms import inlineformset_factory
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView)

from ..decorators import rider_required
from ..forms import RiderSignUpForm, ExecSignUpForm
from ..models import User, Rider, Rides, Executive

class RiderSignUpView(CreateView):
    model = Rider
    form_class = RiderSignUp
    template_name = 'signup.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'rider'

    def form_valid(self, form):
        user = form.save()
        # login(self.request, user)
        return redirect('index.html')