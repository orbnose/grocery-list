from django.test import TestCase
from django.urls import reverse

class TestIndexView(TestCase):
    def test_index(self):
        response = self.client.get(reverse("grocerylist:index"))
        self.assertContains(response, "Grocery Lists")
        self.assertContains(response, "Create new list")