from django.test import TestCase

from ...recipe_entry.unit_conversion import get_unit_model

test_input_labels = [['L', 'litre', 'litres', 'liter', 'liters',], 
                     ['mL', 'millilitre', 'millilitres', 'milliliter', 'milliliters',],
                     ['TSP', 'teaspoon', 'teaspoons',], 
                     ['tbsp', 'tablespoon', 'tablespoons',],
                     ['FL OZ', 'fluid ounce', 'fluid Ounces',],
                     ['c', 'Cup', 'cups',],
                     ['pt', 'pint', 'Pints',],
                     ['qt', 'Quart', 'quarts',],
                     ['gal', 'gallon', 'Gallons',],
                     ['g', 'Gram', 'grams',],
                     ['kg', 'kilogram', 'KiloGrams',],
                     ['OZ', 'ounce', 'ounces',],
                     ['lb', 'lbs', 'Pound', 'pounds'],
                     ]

class TestUnitConversion(TestCase):

    def test_unit_label_conversion(self):
        for label in test_input_labels[0]:
            unit_conversion_assertions(self, label, "liter", "volume")
        
        for label in test_input_labels[1]:
            unit_conversion_assertions(self, label, "milliliter", "volume")
        
        for label in test_input_labels[2]:
            unit_conversion_assertions(self, label, "teaspoon", "volume")
        
        for label in test_input_labels[3]:
            unit_conversion_assertions(self, label, "tablespoon", "volume")
        
        for label in test_input_labels[4]:
            unit_conversion_assertions(self, label, "fluid ounce", "volume")
        
        for label in test_input_labels[5]:
            unit_conversion_assertions(self, label, "cup", "volume")
        
        for label in test_input_labels[6]:
            unit_conversion_assertions(self, label, "pint", "volume")
        
        for label in test_input_labels[7]:
            unit_conversion_assertions(self, label, "quart", "volume")
        
        for label in test_input_labels[8]:
            unit_conversion_assertions(self, label, "gallon", "volume")
        
        for label in test_input_labels[9]:
            unit_conversion_assertions(self, label, "gram", "weight")
        
        for label in test_input_labels[10]:
            unit_conversion_assertions(self, label, "kilogram", "weight")
        
        for label in test_input_labels[11]:
            unit_conversion_assertions(self, label, "ounce", "weight")
        
        for label in test_input_labels[12]:
            unit_conversion_assertions(self, label, "pound", "weight")
            
def unit_conversion_assertions(testcase, input_label: str, correct_unit_label: str, correct_unit_type: str):
    unit = get_unit_model(input_label)
    testcase.assertEqual(unit.name, correct_unit_label)
    testcase.assertEqual(unit.measurement_type, correct_unit_type)