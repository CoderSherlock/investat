"""
Quote live stock/any index's priace hourly

"""
from analysis.models import Live_price
from show.models import Ticker
from yahoo_fin import stock_info
import datetime
from django.utils.timezone import make_aware

"""
Live Quote hourly, saved in analysis.live_price
"""


def quote_live_price():
    all_tickers = Ticker.objects.all()[:]
    for ticker in all_tickers:
        price = round(stock_info.get_live_price(ticker.ticker), 4)
        obj, created = Live_price.objects.update_or_create(
            ticker=ticker,
            defaults={
                'quote_time': make_aware(datetime.datetime.now()),
                'price': price
            }
        )
        obj.save()
