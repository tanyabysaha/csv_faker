from django.urls import path

from mainapp.views import SchemaList, SchemaDelete, SchemaCreate, SchemaUpdate, CsvStatus

urlpatterns = [
    path('', SchemaList.as_view(), name='schema-list'),
    path('<int:id>/delete/', SchemaDelete.as_view(), name='schema-delete'),
    path('create/', SchemaCreate.as_view(), name='schema-create'),
    path('<int:id>/update/', SchemaUpdate.as_view(), name='schema-update'),
    path('status/', CsvStatus.as_view(), name='csv-status'),
]
