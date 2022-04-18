import logging
import datetime as dt

from django.conf import settings
import petl as etl

from sw_collections.models import SWDataCollection
from sw_collections.integrations.swapi import fetch_people_data, fetch_planets_data

logger = logging.getLogger(__name__)


def fetch_new_collection():
    """
    Fetches and saves a new collection
    """
    logger.info('Fetching new collection')
    people_data = fetch_people_data(fetch_planets_data())
    if people_data:
        file_name = str(SWDataCollection.objects.all().count() + 1) + '_' + \
                    dt.datetime.now().strftime('%Y%m%d_%H%M') + '.csv'
        etl.tocsv(people_data, f'{settings.COLLECTIONS_DIR}/{file_name}')
        SWDataCollection.objects.create(data_file=file_name)


def get_collection_data(collection: SWDataCollection, rowcount: int = 10):
    stored_data = etl.fromcsv(f'{settings.COLLECTIONS_DIR}/{collection.data_file}')
    return etl.namedtuples(stored_data.rowslice(rowcount))
