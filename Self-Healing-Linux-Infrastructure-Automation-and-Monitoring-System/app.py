from flask import Flask, render_template
import psutil
import subprocess
import csv

app = Flask(__name__)

@app.route("/")
def dashboard():

    # Current System Metrics
    cpu = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory().percent
    disk = psutil.disk_usage('/').percent

    # Health Score
    health_score = 100

    if cpu > 80:
        health_score -= 20

    if memory > 85:
        health_score -= 20

    if disk > 90:
        health_score -= 20

    # Health Color
    if health_score >= 90:
        health_color = "green"
    elif health_score >= 70:
        health_color = "orange"
    else:
        health_color = "red"

    # Service Monitoring
    services = ["cron"]

    service_status = {}

    for service in services:
        try:
            status = subprocess.check_output(
                ["systemctl", "is-active", service]
            ).decode().strip()

            service_status[service] = status

        except:
            service_status[service] = "unknown"

    # System Uptime
    try:
        with open("/proc/uptime", "r") as f:
            uptime_seconds = int(float(f.readline().split()[0]))
    except:
        uptime_seconds = 0

    uptime_hours = uptime_seconds // 3600

    # Recent Alerts
    alerts = "No Alerts Found"

    try:
        with open("logs/system.log", "r") as f:
            lines = f.readlines()

            if lines:
                alerts = "".join(lines[-10:])
    except:
        pass

    # Last Self-Healing Action
    last_action = "No Actions Performed"

    try:
        with open("logs/healing.log", "r") as f:
            actions = f.readlines()

            if actions:
                last_action = actions[-1]
    except:
        pass

    # Graph Data
    cpu_data = []
    memory_data = []
    disk_data = []

    try:
        with open("metrics/system_metrics.csv", "r") as f:

            reader = csv.reader(f)

            rows = list(reader)[-10:]

            for row in rows:

                if len(row) >= 4:

                    cpu_data.append(float(row[1]))
                    memory_data.append(float(row[2]))
                    disk_data.append(float(row[3]))

    except:
        pass

    return render_template(
        "dashboard.html",
        cpu=cpu,
        memory=memory,
        disk=disk,
        health_score=health_score,
        health_color=health_color,
        uptime_hours=uptime_hours,
        alerts=alerts,
        service_status=service_status,
        last_action=last_action,
        cpu_data=cpu_data,
        memory_data=memory_data,
        disk_data=disk_data
    )

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )
