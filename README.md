# README #

A library that parses multiple images concurrently from Flickr.com and extracts file names and GPS information

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

