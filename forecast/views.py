import requests
from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.http import require_GET, require_POST
from django.db.models import Count
from django.views.decorators.csrf import csrf_exempt

from .models import Search

GEOCODING_URL = 'https://geocoding-api.open-meteo.com/v1/search'
WEATHER_URL = 'https://api.open-meteo.com/v1/forecast'


@csrf_exempt
def home(request):
    ctx = {}
    last = None
    if request.session.session_key:
        last_search = Search.objects.filter(session_key=request.session.session_key).first()
        if last_search:
            last = last_search.city
    if request.method == 'POST':
        city = request.POST.get('city')
        if not city:
            return HttpResponseBadRequest("City required")
        geo = requests.get(GEOCODING_URL, params={'name': city, 'count':5}).json()
        if 'results' not in geo:
            ctx['error'] = 'City not found'
        else:
            loc = geo['results'][0]
            lat, lon = loc['latitude'], loc['longitude']
            # погода на 3 дня
            weather = requests.get(WEATHER_URL, params={
                'latitude': lat, 'longitude': lon,
                'hourly': 'temperature_2m,weathercode',
                'timezone': 'auto'
            }).json()
            ctx['weather'] = weather
            ctx['city'] = loc['name']
            if not request.session.session_key:
                request.session.create()
            Search.objects.create(session_key=request.session.session_key, city=loc['name'])
            ctx['last_city'] = last
            return render(request, 'forecast/home.html', ctx)

@require_GET
def autocomplete(request):
    q = request.GET.get('q','')
    if not q:
        return JsonResponse([], safe=False)
    geo = requests.get(GEOCODING_URL, params={'name': q, 'count':5}).json()
    results = [r['name'] for r in geo.get('results',[])]
    return JsonResponse(results, safe=False)

@require_GET
def search_counts(request):
    qs = Search.objects.values('city').order_by('city').annotate(count=Count('id'))
    data = {item['city']: item['count'] for item in qs}
    return JsonResponse(data)
    