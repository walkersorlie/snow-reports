from django.shortcuts import render


def index(request):
    context = {'response' : "Welcome to your one-stop shop for all Cottonwood snow weather needs"}
    return render(request, 'home/index.html', context)
