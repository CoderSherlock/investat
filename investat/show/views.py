from django import template
from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse
from django.urls import reverse

from .models import Brokerage, Ticker, Transaction
import datetime


def index(request):
    all_transactions = Transaction.objects.order_by('tran_date')[:]
    template = loader.get_template('index.html')
    context = {'transactions': all_transactions}
    return HttpResponse(template.render(context, request))


def transaction_detail(request, transaction_id):
    transaction = Transaction.objects.get(id=transaction_id)
    template = loader.get_template('transaction_detail.html')
    context = {'transaction': transaction}
    return HttpResponse(template.render(context, request))


def add_record(request):
    template = loader.get_template('add_record.html')
    all_tickers = Ticker.objects.all()[:]
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
        tran_date=date,
        brokerage=Brokerage.objects.get(id=brokerageid)
    )
    # except:

    # return HttpResponse("???")

    t.save()
    return HttpResponseRedirect(reverse('index'))


def holdings(request):
    all_transactions = Transaction.objects.order_by('tran_date')[:]
    all_holdings = {}
    for transaction in all_transactions:
        vol = transaction.volume if transaction.trans_type == 'B' else -transaction.volume
        if transaction.ticker not in all_holdings:
            all_holdings[transaction.ticker] = vol
        else:
            all_holdings[transaction.ticker] += vol
    template = loader.get_template('holdings.html')
    context = {'holdings': all_holdings}
    return HttpResponse(template.render(context, request))


def holding_detail(request, ticker):
    ticker_object = Ticker.objects.get(ticker=ticker)
    template = loader.get_template('holding_detail.html')
    transactions = Transaction.objects.filter(ticker=ticker_object).order_by('tran_date')[:]

    holding_amount_change = []
    cost_per_share = 0.0
    cost_per_share_vol = 0.0
    current_vol = transactions[0].volume
    last_date = transactions[0].tran_date
    for transaction in transactions[1:]:
        if (transaction.tran_date != last_date):
            holding_amount_change.append([last_date, current_vol])
        last_date = transaction.tran_date
        if transaction.trans_type == 'B':
            current_vol += transaction.volume
            cost_per_share += transaction.volume * transaction.price
            cost_per_share_vol += transaction.volume
        else:
            current_vol += -transaction.volume      
    holding_amount_change.append([last_date, current_vol])


    context = {'transactions': transactions,
               'ticker': ticker_object,
               'changes_by_date':holding_amount_change,
               'cost_per_share': round(cost_per_share / cost_per_share_vol, 4)}
    return HttpResponse(template.render(context, request))


def dividends(request):
    return HttpResponse("dividends")


def watches(request):
    return HttpResponse("watches")
