from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(User)
admin.site.register(watchlist)
admin.site.register(stock)
admin.site.register(types)
admin.site.register(news)
