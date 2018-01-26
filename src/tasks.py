import json
import requests
import re
from bs4 import BeautifulSoup
from string import ascii_lowercase
from celery import Celery
from helpers import get_url, insert_into_db


app = Celery('tasks', broker='pyamqp://guest@localhost//')
app.conf.update(
    task_routes={
            'tasks.parse_gps': {'queue': 'gps_queue'},
        }
)


@app.task
def parse_gps(photo_json):
    '''
    Parses a photo detail page to get GPS information
    '''

    # Construct url for photo detail page
    url = 'https://www.flickr.com/photos/{}/{}/'.format(photo_json['owner'], photo_json['id'])
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')

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


@app.task
def parse(per_page, page, city):
    '''
    Gets all photos in a particular page for a given city
    And asychronously parses each of these photos to get GPS information
    '''

    page_url = get_url(per_page, page, city)
    response = requests.get(page_url)
    data = json.loads(response.text)
    photos = data.get('photos').get('photo')

    # Enqueue all of the photos into a gps_queue queue
    for photo in photos:
        photo_json = {"city": city, "owner": photo.get('owner'), 'id': photo.get('id')}
        # Get filename/URL
        for c in ascii_lowercase:
            key = 'url_' + c
            if key in photo:
                photo_json['filename'] = photo.get(key)
                break
        parse_gps.delay(photo_json)


@app.task
def parse_city_info(city):
    '''
    Gets the meta info i.e. total number of pages for a city
    And asynchronously parses each of these pages
    '''

    per_page = 100
    page = 1

    url = get_url(per_page, page, city)
    response = requests.get(url)
    data = json.loads(response.text)
    # Get total # of pages
    pages = data.get('photos').get('pages')
    # Enqueue all of the pages into a celery queue
    for i in range(1, int(pages) + 1):
        parse.delay(per_page, i, city)
