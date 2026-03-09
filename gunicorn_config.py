# Gunicorn Configuration File
import multiprocessing
import navconfig

cores = multiprocessing.cpu_count()
APP_HOST = navconfig.config.get('APP_HOST', fallback='0.0.0.0')
APP_PORT = navconfig.config.get('APP_PORT', fallback=5000)
APP_WORKERS = navconfig.config.get('APP_WORKERS', fallback=cores * 2 + 1)

workers = int(APP_WORKERS)
threads = int(navconfig.config.get('APP_THREADS', fallback=4))
max_requests = 1000
max_requests_jitter = 10
bind = f"{APP_HOST}:{APP_PORT}"
backlog = 2048
worker_connections = 1000
timeout = int(navconfig.config.get('APP_TIMEOUT', fallback=360))
keepalive = 2
worker_class = 'aiohttp.worker.GunicornUVLoopWebWorker'
