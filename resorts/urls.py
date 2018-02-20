from django.conf.urls import url

from . import views

app_name = 'resorts'
urlpatterns = [
    url(r'^$', views.index, name = 'index'),
    url(r'^uaac/', views.uaac, name = 'uaac'),
    url(r'^alta/', views.alta, name = 'alta'),
    url(r'^snowbird/', views.snowbird, name = 'snowbird'),
    url(r'^brighton/', views.brighton, name = 'brighton'),
    url(r'^solitude/', views.solitude, name = 'solitude'),
]
