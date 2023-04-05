from ..models import Unit

def get_unit_model(input_label:str):
    unit_label = MEASURES_LOOKUP_TABLE.get(input_label.lower(), MISSING_KEY_VALUE)
    if unit_label == MISSING_KEY_VALUE:
        return None
    return Unit.objects.get(name=unit_label)

MISSING_KEY_VALUE = "NO_UNIT"

MEASURES_LOOKUP_TABLE = {
    "l":        "liter",
    "litre":    "liter",
    "litres":   "liter",
    "liter":    "liter",
    "liters":   "liter",

    "ml":           "milliliter",
    "millilitre":   "milliliter",
    "millilitres":  "milliliter",
    "milliliter":   "milliliter",
    "milliliters":  "milliliter",

    "tsp":          "teaspoon",
    "teaspoon":     "teaspoon",
    "teaspoons":    "teaspoon",

    "tbsp":         "tablespoon",
    "tablespoon":   "tablespoon",
    "tablespoons":  "tablespoon",

    "fl oz":        "fluid ounce",
    "fluid ounce":  "fluid ounce",
    "fluid ounces": "fluid ounce",

    "c":    "cup",
    "cup":  "cup",
    "cups": "cup",

    "pt":       "pint",
    "pint":     "pint",
    "pints":    "pint",

    "qt":       "quart",
    "quart":    "quart",
    "quarts":   "quart",

    "gal":      "gallon",
    "gallon":   "gallon",
    "gallons":  "gallon",

    "g":        "gram",
    "gram":     "gram",
    "grams":    "gram",

    "kg":           "kilogram",
    "kilogram":     "kilogram", 
    "kilograms":    "kilogram",

    "oz":       "ounce",
    "ounce":    "ounce",
    "ounces":   "ounce",

    "lb":       "pound",
    "lbs":      "pound",
    "pound":    "pound",
    "pounds":   "pound",

    "count":    "count",

}