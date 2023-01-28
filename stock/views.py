from turtle import position
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from .models import *
from django.contrib.auth.decorators import login_required
import json
from django.http import JsonResponse
import datetime
from django.utils import timezone
from django.views.generic import ListView, DetailView
from django.db.utils import OperationalError
from datetime import timedelta
from django.views.decorators.csrf import requires_csrf_token
from .forms import *
from django.conf import settings
from django.template.loader import render_to_string
from datetime import date
from nsepy import get_history
from datetime import date
import feedparser
from newsapi import NewsApiClient


# Create your views here.
def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "stock/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "stock/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def index(request):
    if request.user.is_authenticated:

        stocks = stock.objects.all()
        form = CreateMealForm()
        thewatchlists = watchlist.objects.all()
        
        if request.method == 'POST':
            if request.POST.get('oldvalue'):
                theold = request.POST.get('oldvalue')
                thenew = request.POST.get('newvalue')
                thelist = watchlist.objects.get(id= theold)
                thelist.name = thenew
                thelist.save()
                print(theold)
                print(thenew)
            else:
                mealform = CreateMealForm(request.POST)
                mealform.save()
            
        
        return render(request, 'stock/index.html', {'watchlists':thewatchlists, 'form':form, 'stocks': stocks})
    else:
        return HttpResponseRedirect(reverse("login"))

def stocks(request):
    if request.user.is_authenticated:
        NewsFeed = feedparser.parse("https://www.moneycontrol.com/rss/business.xml")

        print ('Number of RSS posts :', len(NewsFeed.entries))

        
        entry = NewsFeed.entries[1]
        print ('Post Title :',entry.title)
        stocks = stock.objects.all()
        return render(request,'stock/stock.html',{'stocks':stocks})
    else:
        return HttpResponseRedirect(reverse("login"))

@csrf_exempt
def addstock(request, id, idd):
    if request.method == 'PUT':
        # print('put')
        # print(id)
        # print(idd)
        data = json.loads(request.body)
        thewatchlist = watchlist.objects.get(id = idd)
        if data.get('add') is not None:
            thestock = stock.objects.get(id = id) 
            thewatchlist.stocks.add(thestock)
        elif data.get('delete') is not None:
            thestock = stock.objects.get(id = id)
            thewatchlist.stocks.remove(thestock)
        elif data.get('deletewatch') is not None:
            # print('ik')
            thewatchlist.delete()
        
    return JsonResponse({"message": "bid added successfully."}, status=201)

def allstocks(request):
    if request.user.is_authenticated:
        form = CreateStock()
        newsapi = NewsApiClient(api_key='4ff0140f52fc49e390a77de5c1aa82d3')


        top_headlines = newsapi.get_everything(q='bitcoin')
        print('ok')
        if request.method == 'POST':
            stockform = CreateStock(request.POST)
            stockform.save()
        
        thestocks = stock.objects.all()
        return render(request, 'stock/allstocks.html',{'stocks':thestocks, 'form':form} )
    else:
        return HttpResponseRedirect(reverse("login"))


def stockinfo(request, iddd):
    thestock = stock.objects.get(id = iddd)
    thenews = news.objects.filter(relatedstock = thestock)
    thestocks = stock.objects.all()
    return render(request, 'stock/stockinfo.html', {'stock':thestock, 'news':thenews, 'stocks':thestocks})


def api(request, idddd):
    thestock = stock.objects.get(id = idddd)
    x = []
    s=date(2023,1,1),
    today = date.today()
    d1 = today.strftime("%Y,%m,%d")
    # print( d1)
    present_date = date.today()

    sbin = get_history(symbol= f'{thestock.symbol}',
                        start=thestock.start,
                        end= thestock.end,         
    )
    
    ssbin = get_history(symbol= f'{thestock.symbol}',
                        start=date.today() - timedelta(days=2),
                        end= date.today(),         
    )
    # print(ssbin)
    
    # data = []
    z = 0
    data = {}
    pickup_records=[]
    for one in sbin.Close.keys():
        pickup_id = sbin.Close.keys()[z]
        pickup_name=sbin.Close.values[z]
        record = {'date':pickup_id, 'close': pickup_name}
    
        pickup_records.append(record) 
        z = z +1
    data["pickup"]=pickup_records

    zz = 0
   
    pickup_recordss=[]
    for one in ssbin.Close.keys():
        pickup_idd = ssbin.Close.keys()[zz]
        pickup_namee=ssbin.Close.values[zz]
        recordd = {'date':pickup_idd, 'current': pickup_namee}
    
        pickup_recordss.append(recordd) 
        zz = zz +1
    data["thecurrent"]=pickup_recordss
 
    return JsonResponse(data)

def thewatchlist(request, watchid):
    if request.user.is_authenticated:
        req_watch = watchlist.objects.get(id=watchid)
        allwatches = watchlist.objects.all()
        print(req_watch.name)
        return render(request, 'stock/watchlist.html', {'watchlist':req_watch, 'watchlists':allwatches})
    else:
        return HttpResponseRedirect(reverse("login"))

def testwatch(request, testwatch):
    req_watch = watchlist.objects.get(id=testwatch)
    data = {}
    pickup_records=[]
    # for stock in req_watch.stocks.all():
    #     sbin = get_history(symbol= f'{stock.symbol}',
    #                     start=stock.start,
    #                     end= stock.end,         
    #     )
    
    #     ssbin = get_history(symbol= f'{stock.symbol}',
    #                         start=date.today() - timedelta(days=1),
    #                         end= date.today(),         
    #     )
    #     z = 0
    
    #     for one in sbin.Close.keys():
    #         pickup_id = sbin.Close.keys()[z]
    #         pickup_name=sbin.Close.values[z]
    #         pickup_current = ssbin.Close.values[z]
    #         record = {'date':pickup_id, 'close': pickup_name, 'current':pickup_current}
        
    #         pickup_records.append(record) 
    #         z = z +1
    #     data["pickup"]=pickup_records

    return render(request, 'stock/testwatch.html')


@csrf_exempt    
def watchfilter(request, watchfilid, currentfrom, currentto, highestfrom, highestto, lowestfrom, lowestto, datefrom, dateto):
    thewatch = watchlist.objects.get(id = watchfilid)
    for object in thewatch.stocks.all():
        sbin = get_history(symbol= f'{object.symbol}',
                        start=object.start,
                        end= object.end,         
        )
    
        ssbin = get_history(symbol= f'{object.symbol}',
                            start=date.today() - timedelta(days=2),
                            end= date.today(),         
        )

        pickup_current = ssbin.Close.values[0]
        print(pickup_current)
        # if (f'{object.start}' == f'{datefrom}') and (f'{object.end}' == f'{dateto}'):
        if (f'{object.start}' == f'{datefrom}') and (f'{object.end}' == f'{dateto}'):

             print('equals')
        print( f'start equals {object.end}')
        print(f' from equals {datefrom}')
        
        
    # thedes = stock.objects.filter(start = datefrom)
    # print(thedes)
    return JsonResponse({"message": "bid added successfully."}, status=201)

def allwatchlists(request):
    if request.user.is_authenticated:
        allwatchlistss = watchlist.objects.all()
        return render(request, 'stock/allwatchlists.html', {'watchlists':allwatchlistss})   
    else:
        return HttpResponseRedirect(reverse("login"))

def stocksnames(request):
    if request.user.is_authenticated:
        stocksnn = stock.objects.all()
        return render(request, 'stock/stocksnames.html', {'stocks':stocksnn})
    else:
        return HttpResponseRedirect(reverse("login"))