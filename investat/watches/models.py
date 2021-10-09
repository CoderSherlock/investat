from django.db import models
import datetime
import django

            

class ETF(models.Model):
    quote_time = models.DateTimeField(default=django.utils.timezone.now)
    ticker = models.CharField(max_length=20)
    
    # Trailing returns
    tr_ytd = models.FloatField(default=0)
    tr_1m = models.FloatField(default=0)
    tr_3m = models.FloatField(default=0)
    tr_1y = models.FloatField(default=0)
    tr_3y = models.FloatField(default=0)
    tr_5y = models.FloatField(default=0)
    tr_10y = models.FloatField(default=0)
    tr_lbull = models.FloatField(default=0)
    tr_lbear = models.FloatField(default=0)

    # Trailing returns of the same category
    tr_ytd_c = models.FloatField(default=0)
    tr_1m_c = models.FloatField(default=0)
    tr_3m_c = models.FloatField(default=0)
    tr_1y_c = models.FloatField(default=0)
    tr_3y_c = models.FloatField(default=0)
    tr_5y_c = models.FloatField(default=0)
    tr_10y_c = models.FloatField(default=0)
    tr_lbull_c = models.FloatField(default=0)
    tr_lbear_c = models.FloatField(default=0)


def batch_insert_etf(filename):
    with open(filename, 'r') as etffile:
        for i in etffile.readlines():
            print(i.strip())
            obj = ETF.objects.create(
                ticker=i.strip()
            )
            obj.save()