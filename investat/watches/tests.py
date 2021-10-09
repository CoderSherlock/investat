from watches.models import batch_insert_etf
from django.test import TestCase


class batch_insert_test(TestCase):
    def test_func_batch_insert_etf(self):
        batch_insert_etf('tmp')
