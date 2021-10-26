from django.contrib import admin

from .models import ETF

class ETFAdmin(admin.ModelAdmin):
    list_display = ('id', 'ticker', 'tr_ytd', 'tr_ytd_c')


admin.site.register(ETF, ETFAdmin)