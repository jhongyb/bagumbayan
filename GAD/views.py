from django.shortcuts import render
from django.http import HttpResponse
import pandas as pd

# Create your views here.
import requests
from django.shortcuts import render
from django.conf import settings

def rbima(request):
    # Get the search term from Project B's search input field
    search_query = request.GET.get('search', '')
    
    # Target Project A's endpoint
    api_url = "http://localhost:1000/api/rbim"
    
    # Forward the search parameter to Project A
    params = {'search': search_query} if search_query else {}
    # Securely authenticate using the token generated in Project A
    headers = {
        "Authorization": f"Token 07a7d9f54843722920b89433d9c8048af1897ede"
    }
    
    try:
        response = requests.get(api_url, headers=headers, params=params, timeout=5)
        response.raise_for_status()
        data = response.json() # This will be the filtered/unfiltered list of records
    except requests.RequestException:
        data = [] # Fallback if Project A is down

    

    return render(request, 'gad.html',{'items': data})


import requests
from django.shortcuts import render
from django.http import HttpResponse

def rbim(request):
    headers = {
        "Authorization": "Token 07a7d9f54843722920b89433d9c8048af1897ede"
    }
    
    try:
        # FIX: Passed the headers into the get request
        stat = requests.get("http://localhost:9000/api/rbims", headers=headers)
        
        if stat.status_code == 200:
            data = stat.json()
            return render(request, 'gad.html', {'items': data})
        else:
            return HttpResponse(f"API Error: Received status code {stat.status_code} | On going Developing Progress contact administrator or developer for more details.", status=stat.status_code)
            
    except requests.exceptions.RequestException as e:
        return HttpResponse(f"<h1 style='text-align:center;padding:10px'>Failed to connect to Bagumbayan Records <br> of \
                            Municipal Inhabitants, Please contact the Administrator or Developer </h1>", status=500)