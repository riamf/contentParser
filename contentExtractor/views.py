from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

import requests
import json
import bs4

@csrf_exempt
def index(request):
    if request.method == 'POST':
        body = request.body.decode('utf-8')
        dictionary = json.loads(body)
        url = dictionary['url']
        response = requests.get(url)
        p = bs4.BeautifulSoup(response.content, 'lxml')
        body = p.find_all('body')
        all_p = []
        all_img = []
        all_h = []
        for b in body:
            all_p += b.find_all('p')
            all_img += b.find_all('img')
            all_h += b.find_all('h1')

        result = {
            "p": [p.text for p in all_p],
            "h": [h.text for h in all_h]
        }
        json_data = json.dumps(result)
        response = HttpResponse(json_data, content_type = "application/json")
        return response

    return HttpResponse('')
