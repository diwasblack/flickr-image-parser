from tasks import parse_city_info
from helpers import create_db


if __name__ == "__main__":
    # Create a database 'flickr.db' if it does not exist
    create_db('flickr.db')
    cities = ['Paris', 'Rome', 'New York']
    # Enqueue photos for each cities into a celery queue
    for city in cities:
        parse_city_info.delay(city)
