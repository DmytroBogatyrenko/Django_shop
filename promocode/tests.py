from django.test import TestCase

from .models import Promocode

# Create your tests here.



class PromocodeModelTest(TestCase):

    def setUp(self):
        self.code = Promocode.objects.create(
            code='CITADEL20',
            value=20,
            valid_date=30,
        )

    def test_str_returns_string(self):
        self.assertIsInstance(str(self.code), str)

    def test_promocode_value_is_saved_correctly(self):
        self.assertEqual(self.code.value, 20)

    def test_promocode_valid_date_default(self):
        self.assertEqual(self.code.valid_date, 30)

    def test_promocode_date_start_is_set_automatically(self):
        self.assertIsNotNone(self.code.date_start)

    def test_unique_codes(self):
        from django.db import IntegrityError
        Promocode.objects.create(code='ANOTHER10', value=10, valid_date=7)
        self.assertEqual(Promocode.objects.count(), 2)