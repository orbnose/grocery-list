import re

from .unit_conversion import get_unit_model
from ..models import Item, Ingredient

regex_ingredient_with_unit_pattern = r"(?P<quantity>[-]?[0-9]+[.,]?[0-9]*([\/][0-9]+[.,]?[0-9]*)*)\s+(?P<unit>l|litre|litres|liter|liters|ml|millilitre|millilitres|milliliter|milliliters|tsp|teaspoon|teaspoons|tbsp|tablespoon|tablespoons|fl oz|fluid ounce|fluid ounces|c|cup|cups|pt|pint|pints|qt|quart|quarts|gal|gallon|gallons|g|gram|grams|kg|kilogram|kilograms|oz|ounce|ounces|lb|lbs|pound|pounds)\s+(?P<item>.+)"
regex_ingredient_no_unit_pattern = r"(?P<quantity>[-]?[0-9]+[.,]?[0-9]*([\/][0-9]+[.,]?[0-9]*)*)\s+(?P<item>.+)"

def extract_ingredient(ingredient_line: str) -> Ingredient:
    ingredient_line = ingredient_line.lower()
    match = re.match(regex_ingredient_with_unit_pattern, ingredient_line)
    if match:
        return get_ingredient(
                    item = match.group('item'), 
                    quantity = match.group('quantity'),
                    unit = get_unit_model(match.group('unit')),
        )
    else:
        match = re.match(regex_ingredient_no_unit_pattern, ingredient_line)
        if match:
            return get_ingredient(
                        item = match.group('item'),
                        quantity = match.group('quantity'),
                        unit = get_unit_model('count'),
            )

def get_ingredient(item, quantity, unit):
    item = get_item(item)
    return Ingredient(item=item, quantity=quantity, unit=unit)

def get_item(item_str: str):
    try:
        item = Item.objects.get(name=item_str)
    except Item.DoesNotExist:
        item = Item(name=item_str)
        item.save()
    return item