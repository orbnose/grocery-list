# grocery-list
Django app for creating grocery lists

## Dependencies
nltk is a dependency. nltk.corpus.words.words() is used for spell checking.

## Quick start
1. Install grocery-list. This should install Django and nltk as dependencies.
```
pip install git+https://github.com/orbnose/grocery-list#egg=grocery-list
```
2. Add the app to the django project's INSTALLED_APPS list.
```
INSTALLED_APPS = [
    ...
    'grocerylist', 
]
```
3. Make the the words corpus is downloaded.
```
python -c "import nltk; nltk.download('words')"
```
4. To use the *common items* button, use the Django admin to create Group objects for the *Produce Front* and *Dairy* sections.

5. Create a sort order in the Django admin for the full list of sections you are targeting in your store.
Ben's personal list:
- Produce Front
- Produce Back
- Cheese Zone
- Dairy
- Bulk
- Canned/Boxed Aisle
- Bread Aisle
- Non-Food
- Frozen
