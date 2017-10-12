from django.shortcuts import render
from goog.models import *
from goog.forms import *
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import re
from django.utils.html import escape

# Create your views here.

def show_results(request, passed_url):
    # if no real link is clicked, go to search page
    raw_uri = request.get_raw_uri()
    search_url = re.search('(?:search).*', raw_uri).group()[7:]
    if len(search_url) < 2:
        searchform = SearchForm()
        return render(request, "search_page.html", {'search_form': searchform})
    else:
        user_agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.101 Safari/537.36'
        headers = {'User-Agent': user_agent}
        result_page = requests.get(search_url, headers)
        page_content = result_page.content.decode(result_page.encoding)
        page_soup = BeautifulSoup(page_content, "html.parser")
        ser_soup = page_soup.find('div', id='res')
        links = [link['href'] for link in ser_soup.find_all('a', href=True)]
        ser_content = str(ser_soup)
        unique_links = set(links)
        for ulink in unique_links:
            if len(ulink) > 3:
                absolute_link = urljoin(search_url, ulink)
                sub_link = '/search/' + escape(absolute_link)
                if ser_content.find(escape(ulink)) == -1:
                    print("Link not found: " + escape(ulink))
                else:
                    print("Link replaced.")
                    ser_content = ser_content.replace(escape(ulink), sub_link)

    context = {'source': ser_content}
    return render(request, "raw_page.html", context)


def process_resulst_and_search_again(request):
    s