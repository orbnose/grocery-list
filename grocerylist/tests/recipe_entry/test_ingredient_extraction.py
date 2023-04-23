from decimal import Decimal

from django.test import TestCase

from ...models import Recipe, Ingredient
from ...recipe_entry.ingredients import extract_ingredient

class TestExtractIngredients(TestCase):
    def setUp(self):
        test_recipe = Recipe(name="Test Recipe")
        test_recipe.save()

    def test_valid_line_with_units(self):
        recipe = Recipe.objects.get(name="Test Recipe")

        input_line = "1 cup rice"
        ingredient = extract_ingredient(input_line, recipe)
        self.assertEqual(ingredient.item.name, "rice")
        self.assertEqual(ingredient.quantity, 1)
        self.assertEqual(ingredient.unit.name, "cup")
        self.assertEqual(ingredient.unit.measurement_type, "volume")

        input_line = "2.5 FL OZ chicken broth"
        ingredient = extract_ingredient(input_line, recipe)
        self.assertEqual(ingredient.item.name, "chicken broth")
        self.assertEqual(ingredient.quantity, 2.5)
        self.assertEqual(ingredient.unit.name, "fluid ounce")
        self.assertEqual(ingredient.unit.measurement_type, "volume")

        input_line = "3 tsp ferMenTed sOy saUce"
        ingredient = extract_ingredient(input_line, recipe)
        self.assertEqual(ingredient.item.name, "fermented soy sauce")
        self.assertEqual(ingredient.quantity, 3)
        self.assertEqual(ingredient.unit.name, "teaspoon")
        self.assertEqual(ingredient.unit.measurement_type, "volume")

        input_line = "1/2 lbs broccoli, chopped"
        ingredient = extract_ingredient(input_line, recipe)
        self.assertEqual(ingredient.item.name, "broccoli, chopped")
        self.assertEqual(ingredient.quantity, 0.5)
        self.assertEqual(ingredient.unit.name, "pound")
        self.assertEqual(ingredient.unit.measurement_type, "weight")

        input_line = "2/3 C pickles"
        ingredient = extract_ingredient(input_line, recipe)
        self.assertEqual(ingredient.item.name, "pickles")
        self.assertEqual(ingredient.quantity, 2.0/3.0)
        self.assertEqual(ingredient.unit.name, "cup")
        self.assertEqual(ingredient.unit.measurement_type, "volume")
    
    def test_valid_line_no_units(self):
        recipe = Recipe.objects.get(name="Test Recipe")

        input_line = "5 broccoli heads"
        ingredient = extract_ingredient(input_line, recipe)
        self.assertEqual(ingredient.item.name, "broccoli heads")
        self.assertEqual(ingredient.quantity, 5)
        self.assertEqual(ingredient.unit.name, "count")
        self.assertEqual(ingredient.unit.measurement_type, "count")

        input_line = "1/3 sliced apple"
        ingredient = extract_ingredient(input_line, recipe)
        self.assertEqual(ingredient.item.name, "sliced apple")
        self.assertEqual(ingredient.quantity, 1/3.0)
        self.assertEqual(ingredient.unit.name, "count")
        self.assertEqual(ingredient.unit.measurement_type, "count")

        input_line = "10 eggs"
        ingredient = extract_ingredient(input_line, recipe)
        self.assertEqual(ingredient.item.name, "eggs")
        self.assertEqual(ingredient.quantity, 10)
        self.assertEqual(ingredient.unit.name, "count")
        self.assertEqual(ingredient.unit.measurement_type, "count")
    
        input_line = "1 loaf bread"
        ingredient = extract_ingredient(input_line, recipe)
        self.assertEqual(ingredient.item.name, "loaf bread")
        self.assertEqual(ingredient.quantity, 1)
        self.assertEqual(ingredient.unit.name, "count")
        self.assertEqual(ingredient.unit.measurement_type, "count")
    
    def test_invalid_lines(self):
        recipe = Recipe.objects.get(name="Test Recipe")

        input_line = "eggs"
        ingredient = extract_ingredient(input_line, recipe)
        self.assertEqual(ingredient, None)

        input_line = "1 1/2 zucchini"
        ingredient = extract_ingredient(input_line, recipe)
        self.assertEqual(ingredient, None)

        input_line = "1 loaf bread\n2.5 cups broth"
        ingredient = extract_ingredient(input_line, recipe)
        self.assertEqual(ingredient, None)

        input_line = "When I was a young warthog, I traipsed the Savannah for 3 days, looking for a source of water."
        ingredient = extract_ingredient(input_line, recipe)
        self.assertEqual(ingredient, None)