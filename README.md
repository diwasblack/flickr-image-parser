# README #

A library that parses multiple images concurrently from Flickr.com and extracts file names and GPS information.

### Tools Used ###
1. Python
2. Celery
3. RabbitMQ
4. unittest

### How to run? ###

Start celery workers for concurrently parsing photos and GPS information.
```sh
$ make start_default_queue_worker
$ make start_gps_queue_worker
```

Start parsing
```sh
$ make start
```

