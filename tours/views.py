# tours/views.py
from django.shortcuts import render
from .models import Tour

def tour_list(request):
    qs = Tour.objects.filter(featured=True)
    return render(request, 'tours/list.html', {'tours': qs})
