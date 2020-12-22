from django.shortcuts import render

# Create your views here.
def index(request):
    text = "Hi..!!"
    return render(request, 'index.html', context={'text':text})

