# Deploying Parrot Autonomous with Supervisord

To ensure `parrot-autonomous` runs robustly in the background and restarts automatically on failure or system reboot, you can manage it using `supervisord`.

## 1. Prerequisites
You need to have `supervisor` installed on your system.

On Ubuntu/Debian:
```bash
sudo apt update
sudo apt install supervisor
```

On Fedora/CentOS/RHEL:
```bash
sudo yum install supervisor
sudo systemctl enable supervisord
sudo systemctl start supervisord
```

## 2. Generate Configuration via CLI
We provide a Python script to automatically construct the supervisord configuration based on your current environment parameters.
Run:

```bash
python scripts/setup_supervisord.py --app-name parrot-autonomous --user your_linux_user
```

**Options:**
- `--app-name`: The identifying name for the application process in supervisor (default: `parrot-autonomous`).
- `--user`: The user context the application will run under.
- `--work-dir`: The project root directory (default: current directory).
- `--conf-dir`: Supervisord's configuration folder (default: `/etc/supervisor/conf.d/`).
- `--reload`: Auto-execute `supervisorctl update` and `supervisorctl start <app-name>` after writing the config.
- `--dry-run`: Prints the generated config to stdout instead of saving it.

## 3. Example Supervisord Configuration
A generated configuration (`/etc/supervisor/conf.d/parrot-autonomous.conf`) looks similar to:

```ini
[program:parrot-autonomous]
command=/path/to/parrot-autonomous/.venv/bin/gunicorn nav:navigator -c gunicorn_config.py
directory=/path/to/parrot-autonomous
user=your_linux_user
autostart=true
autorestart=true
stopasgroup=true
killasgroup=true
stdout_logfile=/path/to/parrot-autonomous/logs/parrot-autonomous_out.log
stderr_logfile=/path/to/parrot-autonomous/logs/parrot-autonomous_err.log
stdout_logfile_maxbytes=50MB
stdout_logfile_backups=5
stderr_logfile_maxbytes=50MB
stderr_logfile_backups=5
```

## 4. Managing the App with supervisorctl

Once the configuration is in place, you can control the application using supervisor's CLI tool:

- Update configuration limits: `sudo supervisorctl update`
- Start the application: `sudo supervisorctl start parrot-autonomous`
- Stop the application: `sudo supervisorctl stop parrot-autonomous`
- Restart the application: `sudo supervisorctl restart parrot-autonomous`
- Check application status: `sudo supervisorctl status parrot-autonomous`
