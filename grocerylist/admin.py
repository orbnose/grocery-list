from django.contrib import admin

from .models import Group, Item, List, Entry
from .models import SortOrder, SortOrderSlot
# Register your models here.

class SortOrderSlotInLine(admin.StackedInline):
    model = SortOrderSlot
    extra = 3

class SortOrderAdmin(admin.ModelAdmin):
    inlines = [SortOrderSlotInLine]

admin.site.register(Group)
admin.site.register(Item)
admin.site.register(List)
admin.site.register(Entry)
admin.site.register(SortOrder, SortOrderAdmin)