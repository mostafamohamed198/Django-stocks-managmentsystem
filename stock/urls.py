from django.urls import path
from .views import *
from . import views
urlpatterns = [
    path('', views.index, name='index'),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path('stocks', views.stocks, name='stocks'),
    path('addstock/<int:id>/<int:idd>',views.addstock, name='addstock'),
    path('allstocks', views.allstocks, name='allstocks'),
    path('stock/<int:iddd>',views.stockinfo, name='stock'),
    path('api/<int:idddd>', views.api, name='api'),
    path('watchlist/<int:watchid>', views.thewatchlist, name='thewatchlist'),
    path('watchfilter/<int:watchfilid>/<int:currentfrom>/<int:currentto>/<int:highestfrom>/<int:highestto>/<int:lowestfrom>/<int:lowestto>/<str:datefrom>/<str:dateto>', views.watchfilter, name='watchfilter'),
    path('allwatchlists', views.allwatchlists, name='allwatchlists'),
    path('stocksnames', views.stocksnames, name='stocksnames')
]   