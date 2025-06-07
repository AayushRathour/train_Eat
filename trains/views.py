from django.shortcuts import render, get_object_or_404
from .models import Train, Station, Platform

# Create your views here.

def train_list(request):
    """View to display a list of all trains."""
    trains = Train.objects.all()
    return render(request, 'trains/train_list.html', {
        'trains': trains
    })

def train_search(request):
    """View to search for trains."""
    query = request.GET.get('q', '')
    trains = Train.objects.filter(number__icontains=query) if query else Train.objects.none()
    return render(request, 'trains/train_search.html', {
        'trains': trains,
        'query': query
    })

def train_detail(request, train_number):
    """View to display details of a specific train."""
    train = get_object_or_404(Train, number=train_number)
    return render(request, 'trains/train_detail.html', {
        'train': train
    })

def train_route(request, train_number):
    """View to display the route of a specific train."""
    train = get_object_or_404(Train, number=train_number)
    return render(request, 'trains/train_route.html', {
        'train': train
    })

def train_location(request, train_number):
    """View to display the current location of a specific train."""
    train = get_object_or_404(Train, number=train_number)
    return render(request, 'trains/train_location.html', {
        'train': train
    })

def station_list(request):
    """View to display a list of all stations."""
    stations = Station.objects.all()
    return render(request, 'trains/station_list.html', {
        'stations': stations
    })

def station_detail(request, station_code):
    """View to display details of a specific station."""
    station = get_object_or_404(Station, code=station_code)
    return render(request, 'trains/station_detail.html', {
        'station': station
    })

def platform_list(request, station_code):
    """View to display platforms of a specific station."""
    station = get_object_or_404(Station, code=station_code)
    platforms = station.platforms.all()
    return render(request, 'trains/platform_list.html', {
        'station': station,
        'platforms': platforms
    })

def platform_detail(request, station_code, platform_number):
    """View to display details of a specific platform."""
    platform = get_object_or_404(Platform, station__code=station_code, number=platform_number)
    return render(request, 'trains/platform_detail.html', {
        'platform': platform
    })
