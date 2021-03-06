"""
Quote index's properties daily

"""
from yahoo_fin import stock_info
import datetime
from django.utils.timezone import make_aware
from watches.models import ETF
import logging

"""
Live Quote hourly, saved in analysis.live_price
"""


def quote_ticker_table():
    logger = logging.getLogger('django')
    all_etfs = ETF.objects.all()[:]
    for etf in all_etfs:
        try:
            data = None
            data = stock_info.get_performance_trailing_returns_and_navprice(etf.ticker)
            logger.debug('[{0}] {1}'.format(etf.ticker, data))
            obj, _ = ETF.objects.update_or_create(
                ticker=etf.ticker,
                defaults={
                    'quote_time': make_aware(datetime.datetime.now()),
                    'tr_ytd': data['trailingReturns']['ytd'],
                    'tr_1m': data['trailingReturns']['oneMonth'],
                    'tr_3m': data['trailingReturns']['threeMonth'],
                    'tr_1y': data['trailingReturns']['oneYear'],
                    'tr_3y': data['trailingReturns']['threeYear'],
                    'tr_5y': data['trailingReturns']['fiveYear'],
                    'tr_10y': data['trailingReturns']['tenYear'],
                    'tr_lbull': data['trailingReturns']['lastBullMkt'],
                    'tr_lbear': data['trailingReturns']['lastBearMkt'],
                    'tr_ytd_c': data['trailingReturnsCat']['ytd'],
                    'tr_1m_c': data['trailingReturnsCat']['oneMonth'],
                    'tr_3m_c': data['trailingReturnsCat']['threeMonth'],
                    'tr_1y_c': data['trailingReturnsCat']['oneYear'],
                    'tr_3y_c': data['trailingReturnsCat']['threeYear'],
                    'tr_5y_c': data['trailingReturnsCat']['fiveYear'],
                    'tr_10y_c': data['trailingReturnsCat']['tenYear'],
                    'tr_lbull_c': data['trailingReturnsCat']['lastBullMkt'],
                    'tr_lbear_c': data['trailingReturnsCat']['lastBearMkt'],

                    'market_price': data['marketPrice'],
                    'nav_price': data['navPrice'],
                }
            )
            obj.save()
        except Exception as e:
            print("ETF {0}'s performance can't be updated ".format(etf.ticker))
            print(e)
            if (data != None):
                obj, _ = ETF.objects.update_or_create(
                    ticker=etf.ticker,
                    defaults={
                        'quote_time': make_aware(datetime.datetime.now()),
                        'tr_ytd': 0,
                        'tr_1m': 0,
                        'tr_3m': 0,
                        'tr_1y': 0,
                        'tr_3y': 0,
                        'tr_5y': 0,
                        'tr_10y': 0,
                        'tr_lbull': 0,
                        'tr_lbear': 0,
                        'tr_ytd_c':0,
                        'tr_1m_c': 0,
                        'tr_3m_c': 0,
                        'tr_1y_c': 0,
                        'tr_3y_c': 0,
                        'tr_5y_c': 0,
                        'tr_10y_c': 0,
                        'tr_lbull_c': 0,
                        'tr_lbear_c': 0,
                    }
                )
                obj.save()

# Test function, will be removed from production
def quote_etf_performance(etf):
    try:
        data = None
        data = stock_info.get_performance_trailing_returns(etf)
        print(data)
    except Exception as e:
        print("ETF {0}'s performance can't be updated ".format(etf))
        print(e)
        if (data != None):
            print('??')
