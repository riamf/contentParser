from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

import requests
import json

@csrf_exempt
def index(request):
    if request.method == 'POST':
        body = request.body.decode('utf-8')
        dictionary = json.loads(body)
        url = dictionary['url']
        response = requests.get(url)
        return HttpResponse(response.content)
    
    return HttpResponse()

