import pytest
import datetime as dt

import petl as etl

from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient

pytestmark = pytest.mark.django_db

from sw_collections.integrations.swapi import fetch_planets_data, fetch_people_data
from sw_collections.utils import fetch_new_collection
from sw_collections.models import SWDataCollection

@pytest.fixture
def rest_client() -> APIClient:
    client = APIClient()
    return client

def test_fetch_planet_data():
    query_result = fetch_planets_data()
    assert query_result['https://swapi.dev/api/planets/1/'] == 'Tatooine'


def test_fetch_people_data():
    planet_data = fetch_planets_data()
    query_result = fetch_people_data(planet_data)
    processed_result = etl.namedtuples(query_result.rowslice(10))
    assert processed_result.len() == 10
    assert processed_result[0].name == 'Luke Skywalker'
    assert processed_result[0].date == dt.date.fromisoformat('2014-12-20')
    assert processed_result[0].homeworld == 'Tatooine'


def test_fetch_new_collection():
    assert SWDataCollection.objects.all().count() == 0
    fetch_new_collection()
    all_collections = SWDataCollection.objects.all()
    assert all_collections.count() == 1
    assert all_collections[0].timestamp.date() == dt.date.today()



