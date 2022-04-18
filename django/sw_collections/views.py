from django.shortcuts import render, redirect, get_object_or_404
from sw_collections.models import SWDataCollection
from sw_collections.utils import fetch_new_collection, get_collection_data
import petl as etl
from django.conf import settings


def dashboard(request):
    return render(request, "base.html")


def collections_list(request):
    collections = SWDataCollection.objects.all()
    return render(request, 'sw_collections/collections_list.html', {'collections_data': collections})


def fetch_data(request):
    # fetch the new data
    fetch_new_collection()
    # redirect user to collections list after fetching
    return redirect('sw_collections:collections_list')


def swdata_collection(request, pk):
    coll = get_object_or_404(SWDataCollection, id=pk)
    rowcount = int(request.GET.get('rows', 10))
    rows_data = get_collection_data(coll, rowcount)
    return render(request, 'sw_collections/collection_detailed.html',
                  {'rows': rows_data, 'nextsize': rowcount + 10, 'collection': pk})
