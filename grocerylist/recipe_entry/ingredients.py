import re
from fractions import Fraction

from .unit_conversion import get_unit_model
from ..models import Item, Ingredient, Recipe

regex_ingredient_with_unit_pattern = r"^(?P<quantity>[-]?[0-9]+[.,]?[0-9]*([\/][0-9]+[.,]?[0-9]*)*)\s+(?P<unit>l|litre|litres|liter|liters|ml|millilitre|millilitres|milliliter|milliliters|tsp|teaspoon|teaspoons|tbsp|tablespoon|tablespoons|fl oz|fluid ounce|fluid ounces|c|cup|cups|pt|pint|pints|qt|quart|quarts|gal|gallon|gallons|g|gram|grams|kg|kilogram|kilograms|oz|ounce|ounces|lb|lbs|pound|pounds)\s+(?P<item>[^\d\\\n]+)$"
regex_ingredient_no_unit_pattern = r"^(?P<quantity>[-]?[0-9]+[.,]?[0-9]*([\/][0-9]+[.,]?[0-9]*)*)\s+(?P<item>[^\d\\]+)$"

def extract_ingredient(ingredient_line: str, recipe: Recipe) -> Ingredient:
    ingredient_line = ingredient_line.lower()
    match_with_unit = re.match(regex_ingredient_with_unit_pattern, ingredient_line)
    if match_with_unit:
        return get_ingredient(
                    item = match_with_unit.group('item'), 
                    quantity = get_quantity(match_with_unit.group('quantity')),
                    unit = get_unit_model(match_with_unit.group('unit')),
                    recipe = recipe,
        )
    else:
        match_no_unit = re.match(regex_ingredient_no_unit_pattern, ingredient_line)
        if match_no_unit:
            return get_ingredient(
                        item = match_no_unit.group('item'),
                        quantity = get_quantity(match_no_unit.group('quantity')),
                        unit = get_unit_model('count'),
                        recipe = recipe,
            )
        else:
            return None

def get_ingredient(item, quantity, unit, recipe):
    item = get_item(item)
    ingredient = Ingredient(item=item, quantity=quantity, unit=unit, recipe=recipe)
    ingredient.save()
    return ingredient

def get_item(item_str: str):
    try:
        item = Item.objects.get(name=item_str)
    except Item.DoesNotExist:
        item = Item(name=item_str)
        item.save()
    return item

def get_quantity(quantity_str: str):
    try:
        return float(quantity_str)
    except ValueError:
        return float(Fraction(quantity_str))