from django.shortcuts import render


def index(request):
    context = {'response' : "Welcome to Wasatch Snow Reports, your one-stop shop for all Cottonwood snow and weather needs. Here you can find snow and weather information for all the Cottonwood Canyon ski resorts as well as backcountry information from the Utah Avalanche Center (UAC)."}
    return render(request, 'home/index.html', context)
