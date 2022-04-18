from django.urls import path
from sw_collections.views import dashboard, collections_list, fetch_data, swdata_collection

app_name = 'sw_collections'

urlpatterns = [
    path('', dashboard, name='dashboard'),
    path('collections_list/', collections_list, name='collections_list'),
    path('fetch_data/', fetch_data, name='fetch_data'),
    path('collection/<int:pk>/', swdata_collection, name='collection-detailed')
]
