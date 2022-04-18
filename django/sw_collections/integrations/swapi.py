import requests
import datetime as dt
import logging
from typing import Tuple, Optional
from http import HTTPStatus

import petl as etl
from django.conf import settings

swapi_params = settings.SWAPI_PARAMS
logger = logging.getLogger(__name__)

def _fetch_planets_page(url) -> Tuple[str, dict]:
    """
    Internal function to parse one page of planet data
    """
    logging.info(f'Fetching {url}')
    result = requests.get(url)
    if not result.status_code == HTTPStatus.OK:
        return None, dict
    parsed_results = {}
    result_data = result.json()
    if result_data.get('count', 0) != 0:
        parsed_results = {p['url']: p['name'] for p in result_data['results']}
    return result_data['next'], parsed_results


def fetch_planets_data() -> dict:

    """
    Synchronous function to fetch the data from all the planets
    Returns with a dict of <url> - <planet> name pairs (for lookup)
    """
    logging.info('Fetching planet data')
    url = swapi_params['base_url'] + swapi_params['planets_url']
    # fetch the first page
    next_url, results = _fetch_planets_page(url)
    # iterate through the other pages
    while next_url is not None:
        next_url, page_results = _fetch_planets_page(next_url)
        results.update(page_results)
    return results


def _fetch_people_page(url) -> Tuple[Optional[str], list]:
    """
    Internal function to fetch a page of people data from SWAPI
    """
    logging.info(f'Fetching people data from url: {url}')
    result = requests.get(url)
    if not result.status_code == HTTPStatus.OK:
        return None, []
    result_data = result.json()
    parsed_results = result_data['results']

    return result_data['next'], parsed_results


def _transform_people_table(raw_data, homeworld_lookup):
    """
    Converts input list to petl table
    """
    parsed_results = etl.fromdicts(raw_data)
    parsed_results = etl.cut(parsed_results,
                             ['name', 'height', 'mass', 'hair_color', 'skin_color', 'eye_color', 'birth_year',
                              'gender', 'homeworld', 'edited'])
    parsed_results = etl.convert(parsed_results, 'homeworld', homeworld_lookup)
    parsed_results = etl.convert(parsed_results, 'edited',
                                 lambda v:dt.datetime.strptime(v, '%Y-%m-%dT%H:%M:%S.%fZ').date())
    parsed_results = etl.rename(parsed_results, 'edited', 'date')
    return parsed_results

def fetch_people_data(homeworld_lookup):
    """
    Function to fetch all data from all people in SWAPI and store them in a petl table
    """
    logging.info(f'Fetching people data')
    # fetch the first page
    url = swapi_params['base_url'] + swapi_params['people_url']
    # fetch the first page
    next_url, results_list = _fetch_people_page(url)
    # iterate through the other pages
    while next_url is not None:
        next_url, page_results = _fetch_people_page(next_url)
        results_list = results_list + page_results

    results_table = _transform_people_table(results_list, homeworld_lookup)
    return results_table
