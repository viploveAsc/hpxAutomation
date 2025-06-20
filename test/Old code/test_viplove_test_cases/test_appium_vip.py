import subprocess
import time
import socket
import pytest
from appium import webdriver
from appium.options.windows import WindowsOptions
from selenium.common.exceptions import NoSuchElementException


def start_winappdriver():
    # Check if something is already listening on port 4723
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        if sock.connect_ex(('127.0.0.1', 4723)) == 0:
            print("✅ WinAppDriver already running.")
            return

    print("🚀 Starting WinAppDriver...")
    subprocess.Popen(
        [r"C:\Program Files (x86)\Windows Application Driver\WinAppDriver.exe"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )

    # Wait for WinAppDriver to be ready
    for _ in range(10):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            if sock.connect_ex(('127.0.0.1', 4723)) == 0:
                print("✅ WinAppDriver is now running.")
                return
        time.sleep(1)
    raise RuntimeError("❌ WinAppDriver failed to start on port 4723.")


@pytest.fixture(scope="module")
def appium_driver():
    start_winappdriver()

    options = WindowsOptions()
    options.app = "AD2F1837.myHP_v10z8vjag6ke6!App"  # AppUserModelId of your UWP app
    options.platform_name = "Windows"
    options.device_name = "WindowsPC"

    driver = webdriver.Remote("http://127.0.0.1:4723", options=options)
    time.sleep(10)
    yield driver
    driver.quit()


def test_click_notifications_and_close(appium_driver):
    driver = appium_driver

    try:
        notif_button = driver.find_element("name", "Notifications")
        notif_button.click()
        print("✅ Clicked Notifications button")
        time.sleep(2)

        close_button = driver.find_element("accessibility id", "SideFlyout.SideFlyoutView.CloseButton")
        close_button.click()
        print("✅ Clicked Close button in flyout")

    except NoSuchElementException as e:
        pytest.fail(f"❌ Element not found: {e}")
    except Exception as e:
        pytest.fail(f"❌ Unexpected error: {e}")


if __name__ == "__main__":
    pytest.main([__file__])
