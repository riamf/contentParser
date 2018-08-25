from django.shortcuts import render
from django.http import HttpResponse

import requests
import concurrent.futures
import json
import bs4

s = requests.Session()

def load_url(url, timeout):
    response = s.get(url, timeout = timeout)
    if response.status_code in range(200,300):
        j = response.json()
        url = j['url']
        resp = requests.get(url)
        if resp.status_code in range(200,300):
            p = bs4.BeautifulSoup(resp.content, 'lxml')
            j['content'] = p.text
        
        return j
        
    return response.json()


# Create your views here.
def index(request):

    content = requests.get('https://hacker-news.firebaseio.com/v0/topstories.json?print=pretty').content
    items = json.loads(content)
    urls = ['https://hacker-news.firebaseio.com/v0/item/{}.json?print=pretty'.format(id) for id in items]

    data = []
    resp_err = 0
    resp_ok = 0
    with concurrent.futures.ThreadPoolExecutor(max_workers=30)   as executor:
        future_to_url = {executor.submit(load_url, url, 10): url for url in urls[:30]}
        for future in concurrent.futures.as_completed(future_to_url):
            url = future_to_url[future]
            try:
                data.append(future.result())
            except Exception as exc:
                resp_err = resp_err + 1
            else:
                resp_ok = resp_ok + 1
    
    if resp_err > 0:
        print("There were some problems {}".format(resp_err))

    response = HttpResponse(json.dumps(data),content_type = 'application/json')
    return response