from django import template
from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse
from django.urls import reverse

from .models import Brokerage, Dividend, Ticker, Transaction
from analysis.models import Live_price
import datetime
import statistics
import json


def index(request):
    all_transactions = Transaction.objects.order_by('-trans_date')[:]
    template = loader.get_template('index.html')
    context = {'transactions': all_transactions}
    return HttpResponse(template.render(context, request))


def transaction_detail(request, transaction_id):
    transaction = Transaction.objects.get(id=transaction_id)
    ticker = Ticker.objects.get(ticker=transaction.ticker)
    template = loader.get_template('transaction_detail.html')
    context = {'transaction': transaction,
               'ticker': ticker}
    return HttpResponse(template.render(context, request))


def add_record(request):
    template = loader.get_template('add_record.html')
    all_tickers = Ticker.objects.order_by('ticker')[:]
    all_brokerages = Brokerage.objects.all()[:]
    context = {}
    context['all_tickers'] = all_tickers
    context['all_brokerages'] = all_brokerages
    return HttpResponse(template.render(context, request))


def add_record_submit(request):
    # try:
    trans_type = request.POST['type']
    tickerid = request.POST['ticker']
    volume = request.POST['volume']
    price = request.POST['price']
    date = request.POST['date']
    brokerageid = request.POST['brokerage']

    t = Transaction.objects.create(
        trans_type=trans_type,
        ticker=Ticker.objects.get(id=tickerid),
        volume=volume,
        price=price,
        trans_date=date,
        brokerage=Brokerage.objects.get(id=brokerageid)
    )
    # except:

    # return HttpResponse("???")

    t.save()
    return HttpResponseRedirect(reverse('transaction index'))


def holdings(request):
    all_transactions = Transaction.objects.order_by('trans_date')[:]
    all_holdings = {}
    for transaction in all_transactions:
        vol = transaction.volume if transaction.trans_type in ('B', 'R') else -transaction.volume
        if transaction.ticker not in all_holdings:
            all_holdings[transaction.ticker] = {'vol': vol}
        else:
            all_holdings[transaction.ticker]['vol'] += vol
    for ticker in all_holdings.keys():
        all_holdings[ticker]['value'] = all_holdings[ticker]['vol'] * Live_price.objects.get(ticker=ticker).price
    template = loader.get_template('holdings.html')
    context = {'holdings': all_holdings}
    return HttpResponse(template.render(context, request))


def holding_detail(request, ticker):
    ticker_object = Ticker.objects.get(ticker=ticker)
    template = loader.get_template('holding_detail.html')
    transactions = Transaction.objects.filter(
        ticker=ticker_object).order_by('trans_date')[:]

    holding_amount_change = []
    cost_per_share = transactions[0].volume * transactions[0].price
    cost_per_share_vol = transactions[0].volume
    current_vol = transactions[0].volume
    last_date = transactions[0].trans_date
    for transaction in transactions[1:]:
        if (transaction.trans_date != last_date):
            holding_amount_change.append([last_date, current_vol])
        last_date = transaction.trans_date
        if transaction.trans_type in ('B', 'R'):
            current_vol += transaction.volume
            if (transaction.trans_type == 'B'):
                cost_per_share += transaction.volume * transaction.price
                cost_per_share_vol += transaction.volume
        else:
            current_vol += -transaction.volume
    holding_amount_change.append([last_date, current_vol])

    context = {'transactions': transactions,
               'ticker': ticker_object,
               'changes_by_date': holding_amount_change,
               'cost_per_share': round(cost_per_share / cost_per_share_vol, 4),
               'current_vol': holding_amount_change[-1][-1]}
    return HttpResponse(template.render(context, request))


def dividends(request):
    all_dividends = Dividend.objects.order_by('-div_date')[:]
    template = loader.get_template('dividend.html')
    context = {'dividends': all_dividends}
    return HttpResponse(template.render(context, request))


def dividend_detail(request, dividend_id):
    dividend = Dividend.objects.get(id=dividend_id)
    ticker = Ticker.objects.get(ticker=dividend.ticker)
    template = loader.get_template('dividend_detail.html')
    context = {'dividend': dividend,
               'ticker': ticker}
    return HttpResponse(template.render(context, request))


def dividend_by_ticker(request, ticker):
    ticker_object = Ticker.objects.get(ticker=ticker)
    template = loader.get_template('holding_detail.html')
    all_dividends = Dividend.objects.filter(
        ticker=ticker_object).order_by('div_date')[:]
    gross_changes = []
    total_dividend = 0.0
    for dividend in all_dividends:
        gross_changes.append([dividend.div_date, dividend.gross_per_share])
        total_dividend += dividend.amount
    template = loader.get_template('dividend_ticker_detail.html')
    context = {'dividends': all_dividends,
               'ticker': ticker_object, 
               'gross_changes': gross_changes,
               'average_gross': round(statistics.mean([x[1] for x in gross_changes]), 4),
               'total_dividend': round(total_dividend, 4)}
    return HttpResponse(template.render(context, request))


def add_dividend_record(request):
    template = loader.get_template('add_dividend.html')
    all_tickers = Ticker.objects.order_by('ticker')[:]
    all_brokerages = Brokerage.objects.all()[:]
    all_transactions = Transaction.objects.order_by('trans_date')[:]
    
    """
    Get current holdings volume for all tickers
    """
    ticker_holding_vol = {}
    for transaction in all_transactions:
        vol = transaction.volume if transaction.trans_type in ('B', 'R') else -transaction.volume
        if transaction.ticker.id not in ticker_holding_vol:
            ticker_holding_vol[transaction.ticker.id] = {'vol': vol}
        else:
            ticker_holding_vol[transaction.ticker.id]['vol'] += vol
        
    context = {}
    context['all_tickers'] = all_tickers
    context['all_brokerages'] = all_brokerages
    context['ticker_holding_vol'] = json.dumps(ticker_holding_vol)
    return HttpResponse(template.render(context, request))

def add_dividend_record_submit(request):
    # try:
    tickerid = request.POST['ticker']
    amount = request.POST['amount']
    gross_per_share = request.POST['gross_per_share']
    date = request.POST['date']

    t = Dividend.objects.create(
        ticker=Ticker.objects.get(id=tickerid),
        amount=amount,
        gross_per_share=gross_per_share,
        div_date=date,
    )
    # except:
    # return HttpResponse("???")
    t.save()
    return HttpResponseRedirect(reverse('dividends'))


