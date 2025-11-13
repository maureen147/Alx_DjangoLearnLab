# Gunicorn Configuration for LibraryProject with HTTPS support

import multiprocessing

# Server socket
bind = "unix:/path/to/your/gunicorn.sock"
backlog = 2048

# Worker processes
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = "sync"
worker_connections = 1000
max_requests = 1000
max_requests_jitter = 50
timeout = 30
keepalive = 2

# Security
limit_request_line = 4096
limit_request_fields = 100
limit_request_field_size = 8190

# Logging
accesslog = "/path/to/your/logs/gunicorn_access.log"
errorlog = "/path/to/your/logs/gunicorn_error.log"
loglevel = "info"

# Process naming
proc_name = "libraryproject"

# Server mechanics
daemon = False
pidfile = "/path/to/your/gunicorn.pid"
umask = 0
user = None
group = None
tmp_upload_dir = None

# SSL (if running Gunicorn directly with SSL)
# keyfile = "/path/to/your/ssl/key.pem"
# certfile = "/path/to/your/ssl/cert.pem"

# Server hooks
def pre_fork(server, worker):
    pass

def post_fork(server, worker):
    server.log.info("Worker %s spawned", worker.pid)

def pre_exec(server):
    server.log.info("Forked child, re-executing.")

def when_ready(server):
    server.log.info("Server is ready. Spawning workers")

def worker_int(worker):
    worker.log.info("Worker received INT or QUIT signal")

def worker_abort(worker):
    worker.log.info("Worker received SIGABRT signal")
