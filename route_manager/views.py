from django.shortcuts import render

# Create your views here.
def index(request):
    # templates/index.html exists at project root templates/, so render that
    return render(request, 'index.html')