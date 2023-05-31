from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from datetime import datetime
from bs4 import BeautifulSoup
import requests
import re
from django.views.decorators.csrf import csrf_exempt
import pandas as pd
def home(request):
    now = datetime.now()
    cur_date = now.strftime('%Y-%m-%d %H:%M:%S')
    return HttpResponse(f'<h2>Hello, Welcome to Django Application<br>'
                        f'The Current Date: { cur_date }</h2>')
def forms(request):
    return render(request,'main.html')

@csrf_exempt
def scrape_prices(request):
    if request.method =='POST':
        search_term = request.POST.get("search_term")
        url = f"https://www.newegg.com/p/pl?d={search_term}&N=4131"
        page = requests.get(url).text
        doc = BeautifulSoup(page, "html.parser")
        page_text = doc.find(class_="list-tool-pagination-text").strong
        pages = int(str(page_text).split("/")[-2].split(">")[-1][:-1])
        items_found = {}
        item_list = []

        for page in range(1, pages + 1):
            url_page = f"https://www.newegg.ca/p/pl?d={search_term}&N=4131&page={page}"
            page = requests.get(url_page).text
            doc = BeautifulSoup(page, "html.parser")

            div = doc.find(class_="item-cells-wrap border-cells items-grid-view four-cells expulsion-one-cell")
            items = div.find_all(text=re.compile(search_term))

            for item in items:
                parent = item.parent
                if parent.name != "a":
                    continue
                link = parent['href']
                next_parent = item.find_parent(class_="item-container")
                try:
                    price = next_parent.find(class_="price-current").find("strong").string
                    rating = next_parent.find(class_="rating rating-4-5")
                    if rating == None:
                        rating = str(rating)
                        rating = "There are no reviews."
                    else:
                        rating = str(rating)[15:33]
                    items_found = {"item": item, "price": int(price.replace(",", "")), "rating": rating, "link": link}
                    item_list.append(items_found)
                except:
                    pass

        sorted_items = sorted(item_list, key=lambda x: x['price'])
        print(sorted_items)
        return render(request,'main.html', {'sorted_items' : sorted_items})
    return render(request, 'input.html')