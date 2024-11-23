import os
import subprocess
import time
from configuration import REMOTE_IP, REMOTE_BASE_COMPOSE_COMMAND, REMOTE_PATH, REMOTE_USER

SERVICE_NAME = os.environ["SERVICE_NAME"]
SERVICE_PORT = os.environ["SERVICE_PORT"]

print(f"SERVICE_NAME: {SERVICE_NAME}")
print(f"SERVICE_PORT: {SERVICE_PORT}")

def check_output(command: str):
    new_command = f"ssh -tt -i ./ssh_key -o 'StrictHostKeyChecking=no' {REMOTE_USER}@{REMOTE_IP} \"cd {REMOTE_PATH} ; {command}\""
    return subprocess.check_output(new_command, shell=True).decode()

container_name = check_output(f"{REMOTE_BASE_COMPOSE_COMMAND} " + "ps --format '{{.Name}}'" + f" {SERVICE_NAME}").strip()
ip = check_output("docker inspect -f '{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}' " + container_name).strip()

print(f"container_name: {container_name}")
print(f"ip: {ip}")

while True:
    print("Connecting ...")
    try:
        os.system(f"ssh -tt -i ./ssh_key -o 'StrictHostKeyChecking=no' -o 'ServerAliveInterval 10' -o 'ServerAliveCountMax 3'" + 
                  " -L 0.0.0.0:{SERVICE_PORT}:{ip}:{SERVICE_PORT} {REMOTE_USER}@{REMOTE_IP} 'while true; do echo running; sleep 10; done;' ;")
    except:
        pass
    time.sleep(1)
