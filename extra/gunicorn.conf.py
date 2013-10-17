bind = "127.0.0.1:8094"
daemon = False
debug = True
workers = 1
logfile = "/var/log/noessay-gunicorn.log"
loglevel = "info"
procname = 'noessay_prod'
pythonpath = "/var/www/noessay_prod"
