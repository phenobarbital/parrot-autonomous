#!/usr/bin/env python3
import argparse
import os
import sys
import subprocess

TEMPLATE = """[program:{app_name}]
command={venv_path}/bin/gunicorn nav:navigator -c gunicorn_config.py
directory={work_dir}
user={user}
autostart=true
autorestart=true
stopasgroup=true
killasgroup=true
stdout_logfile={logs_dir}/{app_name}_out.log
stderr_logfile={logs_dir}/{app_name}_err.log
stdout_logfile_maxbytes=50MB
stdout_logfile_backups=5
stderr_logfile_maxbytes=50MB
stderr_logfile_backups=5
"""

def generate_config(app_name, user, work_dir):
    venv_path = os.path.join(work_dir, ".venv")
    logs_dir = os.path.join(work_dir, "logs")
    
    # Ensure logs dir exists if we can
    if not os.path.exists(logs_dir):
        try:
            os.makedirs(logs_dir, exist_ok=True)
        except OSError:
            pass

    return TEMPLATE.format(
        app_name=app_name,
        venv_path=venv_path,
        work_dir=work_dir,
        user=user,
        logs_dir=logs_dir
    )

def main():
    parser = argparse.ArgumentParser(description="Generate and install Supervisord configuration for Parrot Autonomous.")
    parser.add_argument("--app-name", type=str, default="parrot-autonomous",
                        help="Name of the application in supervisord.")
    parser.add_argument("--user", type=str, required=True,
                        help="The system user that will run the application.")
    parser.add_argument("--work-dir", type=str, default=os.getcwd(),
                        help="Working directory of the application.")
    parser.add_argument("--conf-dir", type=str, default="/etc/supervisor/conf.d",
                        help="Directory where supervisor configuration files are stored.")
    parser.add_argument("--reload", action="store_true",
                        help="Automatically reload supervisor and start the application.")
    parser.add_argument("--dry-run", action="store_true",
                        help="Print the configuration to stdout without saving to the system.")
    
    args = parser.parse_args()

    work_dir = os.path.abspath(args.work_dir)
    config_content = generate_config(args.app_name, args.user, work_dir)

    if args.dry_run:
        print("--- Generated Supervisor Configuration ---")
        print(config_content)
        return

    output_file = os.path.join(args.conf_dir, f"{args.app_name}.conf")

    try:
        # Check if we have write permission, otherwise try using sudo
        if os.access(args.conf_dir, os.W_OK):
            with open(output_file, 'w') as f:
                f.write(config_content)
            print(f"✅ Successfully wrote configuration to {output_file}")
        else:
            print(f"⚠️  No write permission to {args.conf_dir}. Attempting to write with sudo...")
            # Create a temporary file, then sudo cp it into place
            temp_file = f"/tmp/{args.app_name}.conf"
            with open(temp_file, 'w') as f:
                f.write(config_content)
            
            subprocess.run(["sudo", "cp", temp_file, output_file], check=True)
            subprocess.run(["sudo", "chmod", "644", output_file], check=True)
            os.remove(temp_file)
            print(f"✅ Successfully wrote configuration to {output_file} via sudo.")
            
    except Exception as e:
        print(f"❌ Failed to write configuration: {e}")
        sys.exit(1)

    if args.reload:
        print("🔄 Reloading supervisor and starting application...")
        try:
            subprocess.run(["sudo", "supervisorctl", "update"], check=True)
            subprocess.run(["sudo", "supervisorctl", "start", args.app_name], check=True)
            print(f"✅ Application {args.app_name} started.")
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to reload or start supervisor: {e}")
            sys.exit(1)

if __name__ == "__main__":
    main()
