from ..models import Unit

class UnitHolder(object):
    def __init__(self, input_label):
        self.unit_label = self.convertLabel(input_label)
        self.unit = self.getUnit(self.unit_label)
    
    def convertLabel(self, input_label: str):
        input_label = input_label.lower()
        return MEASURES_LOOKUP_TABLE.get(input_label, MISSING_KEY_VALUE)

    def getUnit(self, unit_label: str):
        pass
        #return Unit.objects.get(name=unit_label)
    
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

}