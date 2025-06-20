import subprocess
import time
import requests
from appium import webdriver

def is_appium_running(host='http://127.0.0.1', port=4723):
    try:
        response = requests.get(f"{host}:{port}/status")
        return response.status_code == 200
    except:
        return False

def start_appium():
    if is_appium_running():
        print("Appium server is already running.")
        return

    print("Starting Appium server...")
    # Start Appium as a subprocess
    process = subprocess.Popen(
        ['appium', '--port', '4723'],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        shell=True
    )

    # Wait for server to be up
    timeout = 10
    while timeout:
        if is_appium_running():
            print("Appium server started successfully.")
            break
        time.sleep(1)
        timeout -= 1
    else:
        print("Failed to start Appium server.")

    return process

if __name__ == "__main__":
    appium_process = start_appium()
    # Step 1: Connect to the Windows root session
    root_caps = {
        "platformName": "Windows",
        "deviceName": "WindowsPC",
        "app": "Root"
    }

    driver = webdriver.Remote("http://127.0.0.1:4723", root_caps)
    time.sleep(2)

    # Add your test code here or call other test scripts
    # Step 2: Find the Start button by Name or AutomationId
    try:
        start_button = driver.find_element("name", "Start")  # Or use "AutomationId" if Inspect.exe gives it
        start_button.click()
        print("✅ Start button clicked.")
    except Exception as e:
        print("❌ Could not find or click Start button:", e)

    # To stop the server later:
    appium_process.terminate()
    print("Appium server stopped.")
