from django.db import models

from show.models import Ticker

class Live_price(models.Model):
    quote_time = models.DateTimeField()
    ticker = models.ForeignKey(Ticker, on_delete=models.PROTECT)
    price = models.FloatField(default=0)