from django import template
from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse
from django.urls import reverse

from show.models import Dividend, Transaction, Ticker
from .models import Live_price
from yahoo_fin import stock_info
from .formulas import xirr
import datetime


def index(request):
    all_tickers = Ticker.objects.order_by('ticker')[:]
    all_transactions = Transaction.objects.order_by('trans_date')[:]
    all_dividends = Dividend.objects.order_by('div_date')[:]

    all_holdings = {}
    cost_per_share_price = {}
    cost_per_share_vol = {}
    for transaction in all_transactions:
        if transaction.trans_type in ('B', 'R'):
            vol = transaction.volume

            """
            Calculate cost per share, but not only statistic buying, not reward.
            """
            if (transaction.trans_type == 'B'):
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

        """
        Add volume to holding pool by tickers.
        """
        if transaction.ticker not in all_holdings:
            all_holdings[transaction.ticker] = vol
        else:
            all_holdings[transaction.ticker] += vol

    cost_per_share = {}
    for key, value in cost_per_share_price.items():
        cost_per_share[key] = round(value / cost_per_share_vol[key], 4)

    all_holdings = {key: value for key,
                    value in all_holdings.items() if round(value, 3) != 0}

    # Later used for XIRR
    all_transactions_and_dividend = {key: [] for key in all_holdings.keys()}

    """
    Current market price and update time
    """
    current_prices = {}
    update_time = []
    for holding in all_holdings:
        lp = Live_price.objects.get(ticker=holding)
        current_prices[holding] = round(lp.price, 4)
        update_time.append(lp.quote_time)
    if update_time:
        market_price_update_time = min(update_time)
    else:
        market_price_update_time = datetime.datetime.now()

    """
    Total dividend
    """
    total_dividend = {key: 0 for key in all_holdings.keys()}
    for dividend in all_dividends:
        if (dividend.ticker in total_dividend):
            total_dividend[dividend.ticker] += dividend.amount
            all_transactions_and_dividend[dividend.ticker].append(
                [dividend.div_date, dividend.amount])
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
    return_on_sell_list = [[holding, return_on_sell[holding] - 100] for holding in all_holdings]
    return_on_sell_list = sorted(return_on_sell_list, key=lambda x:x[1])

    """
    Internal return rate
    """
    for transaction in all_transactions:
        if (transaction.ticker in all_transactions_and_dividend):
            all_transactions_and_dividend[transaction.ticker].append(
                [transaction.trans_date, transaction.volume * transaction.price * (-1 if transaction.trans_type == 'B' else 1)])
    for holding in all_transactions_and_dividend:
        all_transactions_and_dividend[holding].append([datetime.date.today(), market_value[holding]])

    xirr_of_holdings = []
    for holding in all_transactions_and_dividend:
        rawdata = all_transactions_and_dividend[holding]
        rawdata = sorted(rawdata, key = lambda x: x[0])
        dateset = [date for [date, _] in rawdata]
        priceset = [price for [_, price] in rawdata]
        xirr_of_holdings.append([holding, xirr(priceset, dateset)])
    
    xirr_of_holdings = sorted(xirr_of_holdings, key=lambda x:x[1])
    # print(xirr_of_holdings)

    template = loader.get_template('analysis_home.html')
    context = {'tickers': all_tickers,
               'cost_per_share': cost_per_share,
               'holdings': all_holdings,
               'current_prices': current_prices,
               'total_dividend': total_dividend,
               'market_value': market_value,
               'return_on_sell': return_on_sell,
               'market_price_update_time': market_price_update_time,
               'xirr_of_holdings': xirr_of_holdings,
               'return_on_sell_list': return_on_sell_list}
    return HttpResponse(template.render(context, request))
