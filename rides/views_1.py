from django.shortcuts import render, redirect
from django.views.generic import CreateView, ListView, UpdateView
from .forms import RiderSignUp, ExecSignUp
from .models import Rider, Executive

# Create your views here.

class RiderSignUpView(CreateView):
    model = Rider
    form_class = RiderSignUp
    template_name = 'signup.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'rider'

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('index.html')

class random(CreateView):
    def index(request):
        text = "Hi..!!"
        return render(request, 'index.html', context={'text':text})

    #def register(request):



    # registered = False

    # if request.method == 'POST':

    #     # Get info from "both" forms
    #     # It appears as one form to the user on the .html page
    #     user_form = Rider(data=request.POST)
        
        

    #     # Check to see both forms are valid
    #     if user_form.is_valid():

    #         if "driver-enable" in request.POST:


    #         # Save User Form to Database
    #         user = user_form.save()

    #         # Hash the password
    #         user.set_password(user.password)

    #         # Update with Hashed password
    #         user.save()

    #         # Now we deal with the extra info!

    #         # Can't commit yet because we still need to manipulate
    #         profile = profile_form.save(commit=False)

    #         # Set One to One relationship between
    #         # UserForm and UserProfileInfoForm
    #         profile.user = user

    #         # Check if they provided a profile picture
    #         if 'profile_pic' in request.FILES:
    #             print('found it')
    #             # If yes, then grab it from the POST form reply
    #             profile.profile_pic = request.FILES['profile_pic']

    #         # Now save model
    #         profile.save()

    #         # Registration Successful!
    #         registered = True

    #     else:
    #         # One of the forms was invalid if this else gets called.
    #         print(user_form.errors,profile_form.errors)

    # else:
    #     # Was not an HTTP post so we just render the forms as blank.
    #     user_form = UserSignUp()

    # # This is the render and context dictionary to feed
    # # back to the registration.html file page.
    # return render(request,'signup.html',
    #                       {'user_form':user_form,
    #                        'registered':registered})

