start_default_queue_worker:
	cd src && celery -A tasks worker -Q celery --loglevel=INFO --autoscale=10,3

start_gps_queue_worker:
	cd src && celery -A tasks worker -Q gps_queue --loglevel=INFO --autoscale=10,3

purge_queue:
	cd src && celery -A tasks purge
	celery -Q gps_queue purge

stop_workers:
	sudo killall celery

start:
	cd src && python main.py
