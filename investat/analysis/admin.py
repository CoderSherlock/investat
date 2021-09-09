from .models import Live_price
from django.contrib import admin

class Live_PriceAdmin(admin.ModelAdmin):
    list_display = ('ticker', 'price', 'quote_time')

admin.site.register(Live_price, Live_PriceAdmin)
