from django.contrib import admin

from .models import Brokerage, Dividend, Operator, Transaction, Ticker


class TransactionAdmin(admin.ModelAdmin):
    list_display = ('ticker', 'volume', 'price', 'trans_type', 'trans_date')


class TickerAdmin(admin.ModelAdmin):
    list_display = ('ticker', 'product_name', 'product_type', 'market_name')


class DividendAdmin(admin.ModelAdmin):
    list_display = ('ticker', 'amount', 'gross_per_share', 'div_date')


admin.site.register(Transaction, TransactionAdmin)
admin.site.register(Ticker, TickerAdmin)
admin.site.register(Dividend, DividendAdmin)
admin.site.register(Operator)
admin.site.register(Brokerage)
