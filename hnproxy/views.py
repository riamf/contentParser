from django.shortcuts import render
from django.http import HttpResponse

import requests
import json
import concurrent.futures

hn_proxy_session = requests.Session()

def index(request):
    return HttpResponse('hnproxy ✅')

def topStories(request):
    urls = _get_top_stories_urls()

    data = []
    resp_err = 0
    resp_ok = 0
    max_stories_to_fetch = 90
    with concurrent.futures.ThreadPoolExecutor(max_workers=30) as executor:
        future_to_url = {executor.submit(_load_url, url, 10, idx): url for idx, url in enumerate(urls[:max_stories_to_fetch])}
        for future in concurrent.futures.as_completed(future_to_url):
            try:
                data.append(future.result())
            except Exception as exc:
                resp_err = resp_err + 1
            else:
                resp_ok = resp_ok + 1
    
    if resp_err > 0:
        print("Problems downloading {} stories".format(resp_err))

    # import pdb; pdb.set_trace();
    response = HttpResponse(json.dumps(sorted(data, key=lambda s: s['order'])),content_type = 'application/json')
    return response

def _get_top_stories_urls():
    response = hn_proxy_session.get('https://hacker-news.firebaseio.com/v0/topstories.json?print=pretty')
    if response.status_code in range(200,300):
        items = response.json()
        urls = ['https://hacker-news.firebaseio.com/v0/item/{}.json?print=pretty'.format(id) for id in items]
        return urls
    else:
        return []

def _load_url(url, timeout, order):
    response = hn_proxy_session.get(url, timeout = timeout)
    json_response = response.json()
    json_response['order'] = order
    return json_response
