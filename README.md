# grocery-list
Django app for creating grocery lists

## Dependencies
nltk is a dependency. nltk.corpus.words.words() is used for spell checking.

## Quick start
1. Make sure nltk is installed and the words corpus is installed.
```
pip install nltk
python -c "import nltk; nltk.download('words')"
```
2. Install grocery-list.
```
pip install git+https://github.com/orbnose/grocery-list#egg=grocery-list
```
3. To use the *common items* button, use the Django admin to create Group objects for the *Produce Front* and *Dairy* sections.

4. Create a sort order in the Django admin for the full list of sections you are targeting in your store.
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
