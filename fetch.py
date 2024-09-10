import cpuinfo
import ctypes
from termcolor import colored
import os
import psutil
import subprocess
import socket
import requests
from datetime import datetime


def get_public_address():
    try:
        response = requests.get("https://api.ipify.org?format=json")
        response.raise_for_status()
        return response.json()["ip"]
    except Exception:
        return None


def get_local_address():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:  
        return None


def get_system_info():
    # OS name and ver
    # I TRIED A LOT TO MAKE THIS BUT COULDN'T. Highly appreciated if someone contributes to make this

    # Username and hostname
    username = os.getlogin()
    hostname = os.uname().nodename
    linelen = len(username) + len(hostname) + 3

    # Uptime
    uptime_seconds = psutil.boot_time()
    current_time = datetime.now()
    boot_time = current_time - datetime.fromtimestamp(uptime_seconds)

    # Calculate uptime in hours and minutes
    uptime_hours = int(boot_time.total_seconds() // 3600)
    uptime_minutes = int((boot_time.total_seconds() % 3600) // 60)

    uptime_str = f"{uptime_hours} hrs, {uptime_minutes} mins"

    # Window Manager (WM)
    wm = os.environ.get("DESKTOP_SESSION") or os.environ.get("XDG_SESSION_TYPE")

    # CPU name
    cpu_info = cpuinfo.get_cpu_info()
    cpu_name = cpu_info["brand_raw"]
    cpu_per = psutil.cpu_percent()

    # Fetching temp
    temp = psutil.sensors_temperatures()['coretemp'][0].current
    temp_str = f"{temp}󰔄"

    # Getting ip addresses
    local_address = get_local_address()
    public_address = get_public_address()


    # Disk space
    disk_usage = psutil.disk_usage("/")
    disk_total = disk_usage.total / (1024 ** 3)
    disk_used = disk_usage.used / (1024 ** 3)
    disk_usage_str = f"{disk_used:.2f} / {disk_total:.2f} GB ({disk_usage.percent:.2f}%)"

    # RAM space
    ram_usage = psutil.virtual_memory()
    ram_total = ram_usage.total / (1024 ** 3)
    ram_used = ram_usage.used / (1024 ** 3)
    ram_usage_str = f"{ram_used:.2f} / {ram_total:.2f} GB ({ram_usage.percent:.2f}%)"


    return {
        colored("", "blue"): colored(f"{username}@{hostname}", "green"),
        colored("", "blue"): cpu_name,
        colored("", "blue"): f"{cpu_per}%",
        colored("", "red"): temp_str,
        colored("󰨇", "blue"): wm,
        colored("", "yellow"): uptime_str,
        colored("", "red"): ram_usage_str,
        colored("", "magenta"): disk_usage_str,
        colored("󰩩", "yellow"): local_address,
        colored("󰩩", "green"): public_address
    }

if __name__ == "__main__":

    system_info = get_system_info()
    print("\n", end="")
    for key, value in system_info.items():
        print(f"  {key}  {value}")

