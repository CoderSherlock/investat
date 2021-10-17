from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .models import ETF


def index(request):
    template = loader.get_template('watch_index.html')
    context = {}
    all_etf_tickers = ETF.objects.all()
    all_etf_tickers = [x.__dict__ for x in all_etf_tickers]
    for etf in all_etf_tickers:
        etf['weight'] = (etf['tr_1m'] + etf['tr_3m'] + etf['tr_ytd'] + etf['tr_1y']
                         )*0.3 + (etf['tr_3y'] + etf['tr_5y'] + etf['tr_10y']) * 0.3
        etf['comp_weight'] = (etf['tr_1m'] - etf['tr_1m_c'] + etf['tr_3m'] - etf['tr_3m_c'] + etf['tr_ytd'] - etf['tr_ytd_c'] +
                              etf['tr_1y'] - etf['tr_1y_c'] + etf['tr_3y'] - etf['tr_3y_c'] + etf['tr_5y'] - etf['tr_5y_c'] + etf['tr_10y'] - etf['tr_10y_c']) / 7
        etf['weight_comp'] = etf['weight'] * 0.6 + etf['comp_weight'] * 0.4

    all_etf_tickers.sort(key=lambda etf: etf['weight_comp'], reverse=True)
    context['etfs'] = all_etf_tickers[:20]
    return HttpResponse(template.render(context, request))

def etf_full_list(request):
    template = loader.get_template('watch_full_list.html')
    context = {}
    all_etf_tickers = ETF.objects.all()
    all_etf_tickers = [x.__dict__ for x in all_etf_tickers]
    for etf in all_etf_tickers:
        etf['weight'] = (etf['tr_1m'] + etf['tr_3m'] + etf['tr_ytd'] + etf['tr_1y']
                         )*0.3 + (etf['tr_3y'] + etf['tr_5y'] + etf['tr_10y']) * 0.3
        etf['comp_weight'] = (etf['tr_1m'] - etf['tr_1m_c'] + etf['tr_3m'] - etf['tr_3m_c'] + etf['tr_ytd'] - etf['tr_ytd_c'] +
                              etf['tr_1y'] - etf['tr_1y_c'] + etf['tr_3y'] - etf['tr_3y_c'] + etf['tr_5y'] - etf['tr_5y_c'] + etf['tr_10y'] - etf['tr_10y_c']) / 7
        etf['weight_comp'] = etf['weight'] * 0.6 + etf['comp_weight'] * 0.4

    all_etf_tickers.sort(key=lambda etf: etf['weight_comp'], reverse=True)
    context['etfs'] = all_etf_tickers
    context['title'] = 'All ETFs'
    return HttpResponse(template.render(context, request))