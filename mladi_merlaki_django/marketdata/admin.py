from django.contrib import admin

from marketdata.models import Stock, Cryptocurrency


admin.site.register(Stock)
admin.site.register(Cryptocurrency)
