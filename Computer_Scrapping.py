import subprocess
import platform
import psutil
import time
import requests
from datetime import datetime

def get_os_info():
    return platform.platform()

def get_system_details():
    details = {
        "computer_type": platform.machine(),
        "cpu_type": platform.processor(),
    }

    details["gpu_info"] = get_gpu_info()
    
    if platform.system() == "Windows":
        try:
            model = subprocess.check_output("wmic csproduct get name", universal_newlines=True)
            details["computer_model"] = model.split("\n")[1].strip()
        except Exception as e:
            details["computer_model"] = "Unknown"
    
    elif platform.system() == "Darwin":
        try:
            model = subprocess.check_output(["system_profiler", "SPHardwareDataType"], universal_newlines=True)
            for line in model.split("\n"):
                if "Model Name" in line or "Model Identifier" in line:
                    details["computer_model"] = line.split(":")[1].strip()
                    break
        except Exception as e:
            details["computer_model"] = "Unknown"
    
    else:
        details["computer_model"] = "Not Specified"
    
    return details

def get_gpu_info():
    """Retrieve GPU information based on the operating system."""
    os_system = platform.system()
    try:
        if os_system == "Windows":
            gpu_info = subprocess.check_output("wmic path win32_VideoController get name", universal_newlines=True)
        elif os_system == "Linux":
            gpu_info = subprocess.check_output("lspci | grep VGA", shell=True, universal_newlines=True)
        elif os_system == "Darwin":
            gpu_info = subprocess.check_output("system_profiler SPDisplaysDataType", shell=True, universal_newlines=True)
        else:
            gpu_info = "Unsupported OS for GPU Info"
    except Exception as e:
        gpu_info = f"Error retrieving GPU Info: {e}"
    return gpu_info

def get_location_from_api(api_token):
    try:
        response = requests.get(f'https://ipinfo.io?token={api_token}')
        location_data = response.json()
        return location_data
    except Exception as e:
        return {"error": str(e)}

def monitor_system(file, interval=60, duration=3600):
    end_time = time.time() + duration
    while time.time() < end_time:
        log_entry = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "cpu_usage": psutil.cpu_percent(),
            "memory_usage": psutil.virtual_memory().percent,
            "disk_usage": psutil.disk_usage('/').percent
        }
        file.write(str(log_entry) + "\n")
        file.flush()
        time.sleep(interval)

def scrapper():
    with open("system_info.txt", "w") as file:
        file.write("System Information:\n")
        os_info = get_os_info()
        system_details = get_system_details()
        file.write(f"Operating System: {os_info}\n")
        for key, value in system_details.items():
            file.write(f"{key}: {value}\n")
            if key == "gpu_info":
                gpu_lines = value.strip().split('\n')
                for line in gpu_lines:
                    file.write(f"GPU: {line.strip()}\n")
        location_info = get_location_from_api('02d299854c35db')
        file.write("\nIP-based Location Information (from API):\n")
        for key, value in location_info.items():
            file.write(f"{key}: {value}\n")
        file.write("\nStarting system monitoring...\n")
        file.flush()
        monitor_system(file=file, interval=10, duration=120)
