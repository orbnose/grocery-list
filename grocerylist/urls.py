from django.urls import path
from . import views

app_name = 'grocerylist'
urlpatterns = [
    path('', views.index, name='index'),
    path('new_list/', views.new_list, name='new_list'),
    path('edit_list/<int:grocList_pk>', views.edit_list, name='edit_list'),
    path('delete_list/<int:grocList_pk>', views.delete_list, name='delete_list'),
    path('add_common_items/<int:grocList_pk>', views.add_common_items, name='add_common_items'),
    path('sort/<int:grocList_pk>', views.sorted_view, name="sort"),
    path('delete_entry/<int:entry_pk>', views.delete_entry, name='delete_entry'),
]