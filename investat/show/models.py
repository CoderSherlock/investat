from django.db import models

TRANSACTION_TYPE = [
    ('S', 'Sell'),
    ('B', 'Buy'),
    ('R', 'Reward'),
]

PRODUCT_TYPE = [
    ('ETF', 'Exchange-traded fund'),
    ('STO', 'Stock'),
    ('OTH', 'Others')
]


class Operator(models.Model):
    operator_name = models.TextField()

    def __str__(self) -> str:
        return self.operator_name


class Ticker(models.Model):
    market_name = models.TextField()
    product_name = models.TextField()
    ticker = models.CharField(max_length=20)
    product_type = models.CharField(
        max_length=3, choices=PRODUCT_TYPE, default='OTH')
    operator_name = models.ForeignKey(
        Operator, on_delete=models.PROTECT, null=True)

    def __str__(self) -> str:
        return self.ticker


class Brokerage(models.Model):
    brokerage_name = models.TextField()

    def __str__(self) -> str:
        return self.brokerage_name


class Transaction(models.Model):
    trans_date = models.DateField('transaction date')
    ticker = models.ForeignKey(Ticker, on_delete=models.PROTECT)
    price = models.FloatField(default=0)
    volume = models.FloatField(default=0)
    trans_type = models.CharField(
        max_length=1, choices=TRANSACTION_TYPE, default='B')
    brokerage = models.ForeignKey(
        Brokerage, on_delete=models.PROTECT, null=True)


class Dividend(models.Model):
    div_date = models.DateField('dividend date')
    ticker = models.ForeignKey(Ticker, on_delete=models.PROTECT)
    amount = models.FloatField(default=0)
    gross_per_share = models.FloatField(default=0)
