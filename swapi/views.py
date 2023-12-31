import requests

from urllib.parse import urlparse, parse_qs

from django.shortcuts import render
from django.views.decorators.http import require_http_methods


def index(request):
    return render(request, 'index.html')

@require_http_methods(['POST'])
def search(request):
    res_items = []
    search = request.POST['search']
    if len(search) == 0:
        return render(request, 'empty.html')

    api_url = f'https://swapi.dev/api/people/?search={search}'

    try:
        response = requests.get(api_url)
        data = response.json()

        if 'results' in data:
            for result in data['results']:
                url = result['url']
                parsed = urlparse(url)
                result['number'] = parsed.path.strip('/').split('/')[-1]
                res_items.append(result)

    except requests.RequestException as e:
        print(f"Error making request to SWAPI: {e}")
    
    return render(request, 'items.html', {'items': res_items, 'result': True})