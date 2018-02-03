import asyncio

from tasks import parse_city_info
from helpers import create_db


if __name__ == "__main__":
    create_db('flickr.db')
    cities = ['Paris', 'Rome', 'New York']

    tasks = []

    for city in cities:
        tasks.append(asyncio.ensure_future(parse_city_info(city)))

    loop = asyncio.get_event_loop()
    loop.run_until_complete(asyncio.wait(tasks))
