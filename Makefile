# Start the main celery worker
start_default_queue_worker:
	cd src && celery -A tasks worker -Q celery --loglevel=INFO --autoscale=10,3

# Start the worker for parsing GPS information and for inserting into db
start_gps_queue_worker:
	cd src && celery -A tasks worker -Q gps_queue --loglevel=INFO --autoscale=10,3

# Remove all elements from queues
purge_queue:
	cd src && celery -A tasks purge
	celery -Q gps_queue purge

# Stop all celery workers
stop_workers:
	sudo killall celery

# Start the main program
start:
	cd src && python main.py

# Run unittests
run_tests:
	cd src && python tests.py -v
