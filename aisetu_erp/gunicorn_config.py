import multiprocessing

# Gunicorn configuration file
# For more info see: https://docs.gunicorn.org/en/stable/configure.html

bind = "0.0.0.0:5004"
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = "sync"
timeout = 120
keepalive = 5

# Logging
accesslog = "gunicorn_access.log"
errorlog = "gunicorn_error.log"
loglevel = "info"

# Process name
proc_name = "aisetu_erp"
