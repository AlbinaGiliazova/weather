from django.test import TestCase, Client
from .models import Search
import json


class ForecastTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_home_get(self):
        """Доступна главная страница."""
        r = self.client.get('/')
        self.assertEqual(r.status_code, 200)

    def test_autocomplete_empty(self):
        """Автозаполнение пустое."""
        r = self.client.get('/autocomplete/')
        self.assertEqual(r.status_code, 200)
        self.assertJSONEqual(r.content, '[]')

    def test_search_counts_initial(self):
        """Число поисков пустое."""
        r = self.client.get('/search_counts/')
        self.assertEqual(r.status_code, 200)
        data = json.loads(r.content)
        self.assertEqual(data, {})

    def test_post_and_history(self):
        """Работает история поисков."""
        Search.objects.create(session_key='abc', city='Moscow')
        r = self.client.get('/search_counts/')
        data = json.loads(r.content)
        self.assertEqual(data.get('Moscow'), 1)
