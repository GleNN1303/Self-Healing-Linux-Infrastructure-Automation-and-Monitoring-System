# Self-Healing Linux Infrastructure Automation and Monitoring System

## Overview

The Self-Healing Linux Infrastructure Automation and Monitoring System is a Linux-based monitoring platform developed using Python, Flask, and Shell Scripting. The system continuously monitors system resources, detects failures, generates alerts, and automatically performs recovery actions to maintain system availability and stability.

## Features

* Real-Time CPU Monitoring
* Memory Usage Monitoring
* Disk Usage Monitoring
* Network Connectivity Monitoring
* Service Health Monitoring (Cron, SSH, MongoDB)
* Automated Service Recovery
* Memory Cleanup Automation
* Disk Cleanup Automation
* Email Alert Notifications
* Security Monitoring (Failed Login Detection)
* Health Score Calculation
* Incident Logging
* Self-Healing Logs
* PDF Report Generation
* Interactive Flask Dashboard
* Performance Trend Graphs

## Technologies Used

* Python
* Flask
* Linux
* Shell Scripting
* Cron Jobs
* Chart.js
* ReportLab
* Psutil
* Yagmail

## Project Architecture

Linux Infrastructure
↓
Monitoring Engine (monitor.py)
↓
CPU | Memory | Disk | Network | Services
↓
Self-Healing Engine
↓
Restart Services | Memory Cleanup | Disk Cleanup
↓
Alerts & Logs
↓
Flask Dashboard & Reports

## Project Structure

self-healing-linux/
├── app.py
├── monitor.py
├── email_alert.py
├── report_generator.py
├── requirements.txt
├── README.md
├── templates/
│ └── dashboard.html
├── scripts/
│ ├── disk_cleanup.sh
│ ├── memory_cleanup.sh
│ └── restart_service.sh
├── logs/
├── metrics/
└── reports/

## Key Functionalities

* Continuously monitors system health and resource utilization.
* Detects service failures and automatically restarts affected services.
* Generates email alerts for critical system events.
* Maintains logs for incidents and self-healing activities.
* Visualizes system performance through a real-time dashboard.
* Generates reports for monitoring and analysis.

## Future Enhancements

* Docker Container Monitoring
* Kubernetes Monitoring
* AI-Based Failure Prediction
* Cloud Infrastructure Integration
* Automated Backup Management

## Author

Subalakshmi K

## Domain

Linux System Administration and DevOps
