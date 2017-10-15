from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render
from goog.models import *
from goog.forms import *
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import re
from django.utils.html import escape
from django.utils import timezone as timezone
from time import sleep
# Create your views here.

@login_required(login_url='/admin/login/')
def process_search(request):
    # check to see if it's GET or POST
    # if it's GET, check to see if the user just hit the link directly (e.g. /search/?$) to start a new search
    # or if the user has clicked a new link within the search results, in which case we need to record the link clicked
    # and the timestamp, then route the student to do a new search
    context = {}
    if request.method == 'GET':
        raw_uri = request.get_raw_uri()
        search_url = re.search('(?:search/).*', raw_uri).group()[7:]
        # check to see if there's something besides /search
        if len(search_url) == 1:
            if search_url == '1' or search_url == '2':
                context['search_engine_choice'] = search_url
            else:
                return HttpResponseRedirect('/search/')
        elif len(search_url) > 1:
            cur_search = Search.objects.filter(student=request.user).last()
            cur_search.next_action_timestamp = timezone.now()
            cur_search.search_url = search_url
            cur_search.save()
            context['message'] = 'Thanks for searching! Please search again!'
            return render(request, "searchchoice.html", context)
        else:
            return HttpResponseRedirect('/searchchoice/')
        context['search_form'] = SearchForm()
        return render(request, "search_page.html", context)
    else:
        user_agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.101 Safari/537.36'
        headers = {'User-Agent': user_agent}
        searchform = SearchForm(request.POST)
        if searchform.is_valid():
            google_root_url = 'https://www.google.com/search?q='
            search_text = searchform.cleaned_data['search_text']
            search_engine_choice = request.POST['search_engine_choice']
            cur_search = Search(student=request.user, search_term=search_text, search_timestamp=timezone.now(),
                                duration_setting=Duration.objects.first().global_duration,
                                search_engine_choice=int(search_engine_choice))
            cur_search.save()
            result_page = requests.get(google_root_url + search_text.replace(' ', '+'), headers)
            page_content = result_page.content.decode(result_page.encoding)
            page_soup = BeautifulSoup(page_content, "html.parser")
            ser_soup = page_soup.find('div', id='res')
            if ser_soup is None:
                return render(request, "raw_page.html", {'google_page': page_content, 'load_delay': 0})
            links = [link['href'] for link in ser_soup.find_all('a', href=True)]
            ser_content = str(ser_soup)
            unique_links = set(links)
            for ulink in unique_links:
                if len(ulink) > 3:
                    absolute_link = urljoin(google_root_url, ulink)
                    sub_link = '/search/' + escape(absolute_link)
                    if ser_content.find(escape(ulink)) != -1:
                        ser_content = ser_content.replace(escape(ulink), sub_link)
        else:
            return render(request, "search_page.html", {'search_form': searchform})
        context = {'source': ser_content}
        context['load_delay'] = Duration.objects.first().global_duration * 1000

        return render(request, "raw_page.html", context)


# def process_resulst_and_search_again(request):
