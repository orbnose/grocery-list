from django.test import TestCase

from ...recipe_entry.conversion import UnitHolder

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
            self.assertEqual(UnitHolder(label).unit_label, "liter")
        
        for label in test_input_labels[1]:
            self.assertEqual(UnitHolder(label).unit_label, "milliliter")
        
        for label in test_input_labels[2]:
            self.assertEqual(UnitHolder(label).unit_label, "teaspoon")
        
        for label in test_input_labels[3]:
            self.assertEqual(UnitHolder(label).unit_label, "tablespoon")
        
        for label in test_input_labels[4]:
            self.assertEqual(UnitHolder(label).unit_label, "fluid ounce")
        
        for label in test_input_labels[5]:
            self.assertEqual(UnitHolder(label).unit_label, "cup")
        
        for label in test_input_labels[6]:
            self.assertEqual(UnitHolder(label).unit_label, "pint")
        
        for label in test_input_labels[7]:
            self.assertEqual(UnitHolder(label).unit_label, "quart")
        
        for label in test_input_labels[8]:
            self.assertEqual(UnitHolder(label).unit_label, "gallon")
        
        for label in test_input_labels[9]:
            self.assertEqual(UnitHolder(label).unit_label, "gram")
        
        for label in test_input_labels[10]:
            self.assertEqual(UnitHolder(label).unit_label, "kilogram")
        
        for label in test_input_labels[11]:
            self.assertEqual(UnitHolder(label).unit_label, "ounce")
        
        for label in test_input_labels[12]:
            self.assertEqual(UnitHolder(label).unit_label, "pound")
            


