import pytest
import pyautogui
import subprocess
import time

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

# Test case for HPX app UI flow
def test_hpx_app_flow(launch_hpx_app):
    # Step 2: Click on the Avatar icon (first click)
    avatar_location = wait_for_image("Avatar.png", timeout=10, confidence=0.8)
    assert avatar_location is not None, "Avatar icon not found for the first click"
    pyautogui.moveTo(avatar_location)
    pyautogui.click()
    time.sleep(1)  # Wait for UI response

    # Step 4: Click on Settings
    settings_location = wait_for_image("Settings.png", timeout=10, confidence=0.8)
    assert settings_location is not None, "Settings icon not found"
    pyautogui.moveTo(settings_location)
    pyautogui.click()
    time.sleep(1)

    # Step 5: Verify the "Terms of Use" link is clickable
    terms_location = wait_for_image("TermsOfUse.png", timeout=10, confidence=0.8)
    assert terms_location is not None, "Terms of Use link not found or not clickable"
    pyautogui.moveTo(terms_location)
    pyautogui.click()
    time.sleep(3)  # Wait for the external browser to open

    # Step 6: Verify the external browser opened for "Terms of Use"
    browser_location = wait_for_image("external_browser.png", timeout=10, confidence=0.8)
    assert browser_location is not None, "External browser did not open as expected"

    print("HPX app automation test completed successfully.")

if __name__ == '__main__':
    pytest.main([__file__])
