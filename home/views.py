from django.shortcuts import render


def index(request):
    context = {'response' : " Welcome to the homepage"}
    return render(request, 'home/index.html', context)
