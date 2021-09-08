from django import template
from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse
from django.urls import reverse

from show.models import Dividend, Transaction, Ticker
from yahoo_fin import stock_info
from asgiref.sync import sync_to_async


def _index(request):
    all_tickers = Ticker.objects.order_by('ticker')[:]
    all_transactions = Transaction.objects.order_by('trans_date')[:]
    all_dividends = Dividend.objects.order_by('div_date')[:]

    all_holdings = {}
    cost_per_share_price = {}
    cost_per_share_vol = {}
    for transaction in all_transactions:
        if transaction.trans_type == 'B':
            vol = transaction.volume

            if (transaction.ticker not in cost_per_share_price):
                cost_per_share_price.setdefault(
                    transaction.ticker, transaction.price * transaction.volume)
                cost_per_share_vol.setdefault(
                    transaction.ticker, transaction.volume)
            else:
                cost_per_share_price[transaction.ticker] += transaction.price * \
                    transaction.volume
                cost_per_share_vol[transaction.ticker] += transaction.volume
        else:
            vol = -transaction.volume
        if transaction.ticker not in all_holdings:
            all_holdings[transaction.ticker] = vol
        else:
            all_holdings[transaction.ticker] += vol

    cost_per_share = {}
    for key, value in cost_per_share_price.items():
        cost_per_share[key] = round(value / cost_per_share_vol[key], 4)

    all_holdings = {key: value for key,
                    value in all_holdings.items() if value != 0}

    """
    Current market price
    """
    current_prices = {}
    for holding in all_holdings:
        current_prices[holding] = round(
            stock_info.get_live_price(holding.ticker), 4)

    """
    Total dividend
    """
    total_dividend = {key: 0 for key in all_holdings.keys()}
    for dividend in all_dividends:
        if (dividend.ticker in total_dividend):
            total_dividend[dividend.ticker] += dividend.amount
    total_dividend = {key: round(value, 4)
                      for key, value in total_dividend.items()}

    """
    Market value
    """
    market_value = {}
    for holding in all_holdings:
        market_value[holding] = current_prices[holding] * all_holdings[holding]
    market_value = {key: round(value, 4)
                    for key, value in market_value.items()}

    """
    Return on sell
    """
    return_on_sell = {}
    for holding in all_holdings:
        return_on_sell[holding] = round((
            market_value[holding] + total_dividend[holding]) / 
            (cost_per_share[holding] * all_holdings[holding]) * 100, 2)

    template = loader.get_template('analysis_home.html')
    context = {'tickers': all_tickers,
               'cost_per_share': cost_per_share,
               'holdings': all_holdings,
               'current_prices': current_prices,
               'total_dividend': total_dividend,
               'market_value': market_value,
               'return_on_sell': return_on_sell}
    return HttpResponse(template.render(context, request))

index = sync_to_async(_index, thread_sensitive=True)