import time
import pyautogui
import subprocess
import pytest

VERSION_LABEL_IMG = 'Version.png'

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

    # Step 5: Validate version is in read-only mode (not interactive)
    version_location = wait_for_image("Version.png", timeout=10, confidence=0.8)
    assert version_location is not None, 'Version label was not found in About section'

    # Move to version label and click
    pyautogui.moveTo(version_location)
    pyautogui.click()
    time.sleep(2)  # Wait briefly to observe any UI change

    # Take screenshot of a broader area to detect any visual changes
    x = int(version_location[0])
    y = int(version_location[1])
    before = pyautogui.screenshot(region=(x - 100, y - 50, 200, 100))
    time.sleep(2)
    after = pyautogui.screenshot(region=(x - 100, y - 50, 200, 100))

    # Simple visual comparison
    if before.tobytes() != after.tobytes():
        pytest.fail("Version label appears to be interactive, screen content changed after clicking it.")
    else:
        print("Version label is not interactive as expected.")

if __name__ == '__main__':
    pytest.main([__file__])
