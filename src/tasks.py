import json
import re
import logging

from aiohttp import ClientSession
from bs4 import BeautifulSoup
from string import ascii_lowercase
from helpers import get_url, insert_into_db

logging.basicConfig(
    format='%(asctime)s %(levelname)s %(message)s', level=logging.DEBUG)
logger = logging.getLogger(__name__)


async def parse_gps(photo_json):
    '''
    Parses a photo detail page to get GPS information
    '''

    logger.debug("Parsing GPS info for city: {} photo id: {}".format(
        photo_json['city'], photo_json['id']))

    # Construct url for photo detail page
    url = 'https://www.flickr.com/photos/{}/{}/'.format(
        photo_json['owner'], photo_json['id'])

    async with ClientSession() as session:
        async with session.get(url) as response:
            page = await response.text()

            soup = BeautifulSoup(page, 'html.parser')

            # GPS information is stored in javascript. Get that part
            results = soup.find('script', attrs={'class': 'modelExport'})
            rstr = results.text

            long_regex = re.compile("\"longitude\":(([^,])*),")
            lat_regex = re.compile("\"latitude\":(([^,])*),")

            longitude = long_regex.search(rstr).group(1)
            latitude = lat_regex.search(rstr).group(1)

            # Create a row to be inserted into db
            row = (photo_json['filename'], longitude, latitude)

            return insert_into_db(row)


async def parse(per_page, page, city):
    '''
    Gets all photos in a particular page for a given city
    And asychronously parses each of these photos to get GPS information
    '''

    logger.debug("Parsing page {} for city: {}".format(page, city))

    page_url = get_url(per_page, page, city)
    async with ClientSession() as session:
        async with session.get(page_url) as response:
            response = await response.text()
            data = json.loads(response)
            photos = data.get('photos').get('photo')

            for photo in photos:
                photo_json = {"city": city, "owner": photo.get(
                    'owner'), 'id': photo.get('id')}
                # Get filename/URL
                for c in ascii_lowercase:
                    key = 'url_' + c
                    if key in photo:
                        photo_json['filename'] = photo.get(key)
                        break
                await parse_gps(photo_json)


async def parse_city_info(city):
    '''
    Gets the meta info i.e. total number of pages for a city
    And asynchronously parses each of these pages
    '''

    logger.debug("Getting meta data from city: {}".format(city))

    per_page = 1
    page = 1

    url = get_url(per_page, page, city)
    async with ClientSession() as session:
        async with session.get(url) as response:
            response = await response.text()
            data = json.loads(response)
            pages = data.get('photos').get('pages')
            for i in range(1, int(pages) + 1):
                await parse(per_page, i, city)
