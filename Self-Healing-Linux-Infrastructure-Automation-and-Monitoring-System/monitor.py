import psutil
import os
import subprocess
from datetime import datetime
from email_alert import send_alert

LOG_FILE = "logs/system.log"
HEALING_LOG = "logs/healing.log"
METRICS_FILE = "metrics/system_metrics.csv"

os.makedirs("logs", exist_ok=True)
os.makedirs("metrics", exist_ok=True)

def log_message(msg):
    with open(LOG_FILE, "a") as f:
        f.write(f"[{datetime.now()}] {msg}\n")

def healing_message(msg):
    with open(HEALING_LOG, "a") as f:
        f.write(f"[{datetime.now()}] {msg}\n")

def check_service(service):
    try:
        result = subprocess.run(
            ["systemctl", "is-active", service],
            capture_output=True,
            text=True
        )
        return result.stdout.strip()
    except:
        return "unknown"

def check_failed_logins():
    try:
        with open("/var/log/auth.log", "r") as f:
            lines = f.readlines()

        failed = 0

        for line in lines[-200:]:
            if "Failed password" in line:
                failed += 1

        return failed

    except:
        return 0

print("\n===== SELF HEALING SYSTEM =====")

health_score = 100

# CPU Monitoring
cpu = psutil.cpu_percent(interval=1)

print(f"CPU Usage: {cpu}%")

if cpu > 80:

    log_message(f"ALERT: High CPU Usage ({cpu}%)")

    try:
        send_alert(
            "CPU Alert",
            f"CPU Usage is {cpu}%"
        )
    except:
        pass

    health_score -= 20

# Memory Monitoring
memory = psutil.virtual_memory().percent

print(f"Memory Usage: {memory}%")

if memory > 85:

    log_message(
        f"ALERT: High Memory Usage ({memory}%)"
    )

    try:
        send_alert(
            "Memory Alert",
            f"Memory Usage is {memory}%"
        )
    except:
        pass

    subprocess.run(
        ["sudo", "bash", "scripts/memory_cleanup.sh"]
    )

    healing_message(
        "Memory Cleanup Executed"
    )

    health_score -= 20

# Disk Monitoring
disk = psutil.disk_usage('/').percent

print(f"Disk Usage: {disk}%")

if disk > 90:

    log_message(
        f"ALERT: Disk Usage Critical ({disk}%)"
    )

    try:
        send_alert(
            "Disk Alert",
            f"Disk Usage is {disk}%"
        )
    except:
        pass

    subprocess.run(
        ["sudo", "bash", "scripts/disk_cleanup.sh"]
    )

    healing_message(
        "Disk Cleanup Executed"
    )

    health_score -= 20

# Service Monitoring
services = ["cron", "ssh", "mongod"]

for service in services:

    status = check_service(service)

    print(f"{service}: {status}")

    if status != "active":

        log_message(
            f"ALERT: {service} Service Down"
        )

        try:
            send_alert(
                "Service Failure",
                f"{service} service is down"
            )
        except:
            pass

        subprocess.run(
            [
                "sudo",
                "bash",
                "scripts/restart_service.sh",
                service
            ]
        )

        healing_message(
            f"Restarted {service}"
        )

        health_score -= 10

# Internet Check
network = os.system(
    "ping -c 1 8.8.8.8 > /dev/null 2>&1"
)

if network == 0:
    print("Internet Status: Connected")

else:

    print("Internet Status: Disconnected")

    log_message(
        "ALERT: Internet Connection Failed"
    )

    health_score -= 10

# Zombie Process Check
zombies = []

for proc in psutil.process_iter(
    ['pid', 'name', 'status']
):

    if proc.info['status'] == psutil.STATUS_ZOMBIE:
        zombies.append(proc.info)

if zombies:

    print(
        f"Zombie Processes Found: {len(zombies)}"
    )

    log_message(
        f"ALERT: {len(zombies)} Zombie Processes Found"
    )

    health_score -= 10

else:

    print("Zombie Processes: None")

# Failed Login Detection
failed_logins = check_failed_logins()

print(
    f"Failed Login Attempts: {failed_logins}"
)

if failed_logins > 5:

    log_message(
        f"SECURITY ALERT: {failed_logins} Failed Login Attempts"
    )

    try:
        send_alert(
            "Security Alert",
            f"{failed_logins} Failed Login Attempts Detected"
        )
    except:
        pass

    health_score -= 10

# Load Average
load1, load5, load15 = os.getloadavg()

cpu_count = os.cpu_count()

print(f"Load Average: {load1}")

if load1 > cpu_count:

    log_message(
        f"ALERT: High Load Average ({load1})"
    )

    health_score -= 10

# Save Metrics
with open(METRICS_FILE, "a") as f:

    f.write(
        f"{datetime.now()},{cpu},{memory},{disk}\n"
    )

# Final Score
print(f"\nHealth Score: {health_score}/100")

print("\nMonitoring Completed Successfully")
