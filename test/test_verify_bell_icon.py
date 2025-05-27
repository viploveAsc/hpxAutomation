import time
import pyautogui
import subprocess
import pytest

screenshot_path = "screenshot/"

# Helper function to wait for an image to appear on the screen
def wait_for_image(image, timeout=10, confidence=0.8):
    start_time = time.time()
    while True:
        location = pyautogui.locateCenterOnScreen(image, confidence=confidence)
        if location:
            return location
        if time.time() - start_time > timeout:
            return None
        time.sleep(1)

# Fixture to launch the HPX application
@pytest.fixture(scope='module')
def launch_hpx_app():
    # Step 1: Launch HPX app
    # Replace "HPX_app_id!App" with the actual app identifier
    app_id = "AD2F1837.myHP_v10z8vjag6ke6!App"
    subprocess.Popen(f'explorer shell:AppsFolder\\{app_id}', shell=True)
    time.sleep(5)  # Wait for the app to fully open
    yield
    # Optional teardown can go here

# Test case 1 for HPX app UI flow to test bell notification is present
def test_tc_3_bell_notifications_bell_icon_can_be_clicked(launch_hpx_app):
    # Locate and click bell icon
    bell_icon = pyautogui.locateCenterOnScreen(screenshot_path + "bell_icon.png", confidence=0.8)
    if bell_icon:
        pyautogui.moveTo(bell_icon)
        pyautogui.click()
        print("Clicked on bell icon!")
        time.sleep(5)
        # Uncomment below if needed for closing notification
        # close_btn = pyautogui.locateCenterOnScreen(screenshot_path + "close_btn.png", confidence=0.7)
        # pyautogui.moveTo(close_btn)
        # pyautogui.click()
    else:
        print("Bell icon not found!")

if __name__ == '__main__':
    pytest.main([__file__])
