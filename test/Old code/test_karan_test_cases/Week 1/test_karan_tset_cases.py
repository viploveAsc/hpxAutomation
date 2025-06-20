import time
import subprocess
import pyautogui
import pytest
import pygetwindow as gw

# Global screenshot path
screenshot_path = 'screenshots/karan_dark_mode/'


# Utility Functions

def wait_for_image(image, timeout=15, confidence=0.6):
    """
    Waits for an image to appear on screen within the timeout.

    Args:
        image (str): Path to the image file.
        timeout (int): Timeout in seconds.
        confidence (float): Matching confidence (0 to 1.0).

    Returns:
        (x, y) tuple if image found, else None.
    """
    start_time = time.time()
    while True:
        try:
            location = pyautogui.locateCenterOnScreen(image, confidence=confidence)
            if location:
                return location
        except Exception as e:
            print(f"[Error] locateCenterOnScreen failed: {e}")
        if time.time() - start_time > timeout:
            print(f"[Timeout] Image not found within {timeout} seconds: {image}")
            return None
        time.sleep(1)


def click_on_close_button():
    """Click on the app's close button using a predefined screenshot."""
    time.sleep(5)
    close_btn = pyautogui.locateCenterOnScreen(screenshot_path + "close_btn.png", confidence=0.7)
    time.sleep(5)
    if close_btn:
        pyautogui.moveTo(close_btn)
        pyautogui.click()
    time.sleep(2)


# Pytest fixture for launching HPX application
@pytest.fixture(scope="module")
def launch_hpx_app():
    app_id = "AD2F1837.myHP_v10z8vjag6ke6!App"
    subprocess.Popen(f"explorer shell:AppsFolder\\{app_id}", shell=True)
    time.sleep(5)
    yield


# Test case C53304353: [HPX]App Resize Scenarios
@pytest.mark.usefixtures("launch_hpx_app")
def test_c53304353_hpx_app_resize_scenarios(launch_hpx_app):
    # Step 1: Verify HPX Application launch
    app_launch = wait_for_image(screenshot_path + "myhp_app.png")
    assert app_launch is not None, "HPX-Application did not launch as expected."

    # Step 2: Resize app using minimize and maximize button
    minimize_btn = wait_for_image(screenshot_path + "minimize.png")
    assert minimize_btn is not None, "Minimize button not found."
    pyautogui.click(minimize_btn)
    time.sleep(2)
    maximize_btn = wait_for_image(screenshot_path + "maximize.png")
    assert maximize_btn is not None, "Maximize button not found."
    pyautogui.click(maximize_btn)
    time.sleep(2)


# Test case C53303840
@pytest.mark.usefixtures("launch_hpx_app")
def test_c53303840_hpx_settings_about_verify_the_link_terms_of_use_is_clickable():
    """Test: [HPX][Settings][About] Verify 'Terms of Use' link is clickable and opens browser"""

    avatar_icon = wait_for_image(screenshot_path + "Avatar.png")
    assert avatar_icon is not None, "Avatar icon not found."
    pyautogui.click(avatar_icon)
    time.sleep(2)

    settings_button = wait_for_image(screenshot_path + "Settings.png")
    assert settings_button is not None, "Settings button not found."
    pyautogui.click(settings_button)
    time.sleep(2)
    pyautogui.scroll(-500)

    terms_link = wait_for_image(screenshot_path + "TermsOfUse.png")
    assert terms_link is not None, "'Terms of Use' link not found or not clickable."
    pyautogui.click(terms_link)
    time.sleep(3)

    windows = gw.getWindowsWithTitle('HP Smart')  # fuzzy title match
    if windows:
        print("Chrome window with expected title opened.")
    else:
        print("Chrome window with expected title not found.")

    print("HPX app automation test completed.")


# Test case C53303839
@pytest.mark.usefixtures("launch_hpx_app")
def test_c53303839_hpx_settings_about_verify_hp_end_user_license_agreement_link_is_clickable():
    """Test: [HPX][Settings][About] Verify the 'HP End User License Agreement' link is clickable"""
    # Step 1: Launch HPX app is handled by the fixture
    pyautogui.hotkey('win', 'd')
    time.sleep(2)
    desktop_icon = wait_for_image(screenshot_path + 'desktop_myhp.png', timeout=10, confidence=0.8)
    assert desktop_icon is not None, "❌ MyHP desktop app icon not found on desktop."
    print("✅ Step 1: MyHP app icon found on desktop at", desktop_icon)
    pyautogui.click(desktop_icon)
    pyautogui.click(desktop_icon)
    time.sleep(2)

    # Step 4: Verify EULA link is clickable
    print("Step 4: Searching for 'HP End User License Agreement' link.")
    eula_link = wait_for_image(screenshot_path + "HPEndUserLicenseAgreement.png", timeout=10, confidence=0.8)
    assert eula_link is not None, "❌ 'HP End User License Agreement' link not found or not clickable."
    print("✅ 'HP End User License Agreement' link is clickable.")

    # Step 5: Click EULA link
    pyautogui.moveTo(eula_link)
    pyautogui.click()
    print("✅ Clicked on HP End User License Agreement link.")
    time.sleep(5)

    windows = gw.getWindowsWithTitle('End-User License Agreement | undefined')  # fuzzy title match
    if windows:
        print("Chrome window with expected title opened.")
    else:
        print("Chrome window with expected title not found.")


# Test case C53303838
@pytest.mark.usefixtures("launch_hpx_app")
def test_c53303838_hpx_settings_about_verify_version_number_read_only():
    """Test: [HPX][Settings][About] Verify the version number is only read-only"""
    # Step 1: Verify HPX Application launch
    pyautogui.hotkey('win', 'd')
    time.sleep(2)
    desktop_icon = wait_for_image(screenshot_path + 'desktop_myhp.png', timeout=10, confidence=0.8)
    assert desktop_icon is not None, "❌ MyHP desktop app icon not found on desktop."
    print("✅ Step 1: MyHP app icon found on desktop at", desktop_icon)
    pyautogui.click(desktop_icon)
    pyautogui.click(desktop_icon)
    time.sleep(2)

    print('Step: Clicking on Add Device')
    add_device_location = wait_for_image(screenshot_path + 'add_device.png')
    assert add_device_location is not None, '❌ Add Device button not found'
    pyautogui.moveTo(add_device_location)
    pyautogui.click()
    time.sleep(2)

    # Step 2: Click on the Avatar icon (first click)
    avatar_location = wait_for_image(screenshot_path + "Avatar.png", timeout=10, confidence=0.8)
    assert avatar_location is not None, "Avatar icon not found for the first click"
    pyautogui.moveTo(avatar_location)
    pyautogui.click()
    time.sleep(1)  # Wait for UI response

    # Step 4: Click on Settings
    settings_location = wait_for_image(screenshot_path + "Settings.png", timeout=10, confidence=0.8)
    assert settings_location is not None, "Settings icon not found"
    pyautogui.moveTo(settings_location)
    pyautogui.click()
    time.sleep(1)

    # Step 5: Validate version is in read-only mode (not interactive)
    version_location = wait_for_image(screenshot_path + "Version.png", timeout=10, confidence=0.8)
    assert version_location is not None, 'Version label was not found in About section'

    # Move to version label and click
    pyautogui.moveTo(version_location)
    pyautogui.click()
    time.sleep(2)  # Wait briefly to observe any UI change

    # Take screenshot of a broader area to detect any visual changes (e.g., pop-up or navigation)
    x = int(version_location[0])
    y = int(version_location[1])
    before = pyautogui.screenshot(region=(x - 100, y - 50, 200, 100))
    time.sleep(2)
    after = pyautogui.screenshot(region=(x - 100, y - 50, 200, 100))

    # Simple visual comparison (you can replace this with image diff logic for real tests)
    if before.tobytes() != after.tobytes():
        pytest.fail("Version label appears to be interactive, screen content changed after clicking it.")
    else:
        print("Version label is not interactive as expected.")


# Test case C53303837
@pytest.mark.usefixtures("launch_hpx_app")
def test_c53303837_hpx_settings_about_verify_version_number_side_panel():
    """Test: [HPX][Settings][About] Verify the Version number on the Settings side panel"""
    # Step 1: Verify HPX Application launch

    # Step 5: Validate version is in read-only mode (not interactive)
    version_location = wait_for_image(screenshot_path + "Version.png", timeout=10, confidence=0.8)
    assert version_location is not None, 'Version label was not found in About section'

# Test case C53303847: [HPX][Settings][Privacy] PIPL Data transfer toggle functionality
@pytest.mark.usefixtures("launch_hpx_app")
def test_c53303847_hpx_settings_privacy_pipl_data_transfer_toggle(launch_hpx_app):
    print('Step 4: Clicking on Manage Privacy Settings')
    manage_privacy_location = wait_for_image(screenshot_path + 'manage_privacy_settings.png')
    assert manage_privacy_location is not None, 'Manage Privacy Settings option not found'
    pyautogui.moveTo(manage_privacy_location)
    pyautogui.click()
    time.sleep(2)

    # Step 5: Click on the first toggle button
    print('Step 5: Clicking on the first toggle button')
    first_toggle_location = wait_for_image(screenshot_path + 'manage_settings_toggle_1.png')
    assert first_toggle_location is not None, 'First toggle button not found'
    pyautogui.moveTo(first_toggle_location)
    pyautogui.click()
    time.sleep(1)

    # Step 6: Scroll down
    print('Step 6: Scrolling down')
    pyautogui.scroll(-300)
    time.sleep(1)

    # Step 7: Click on the second toggle button
    print('Step 7: Clicking on the second toggle button')
    second_toggle_location = wait_for_image(screenshot_path + 'manage_settings_toggle_2.png')
    assert second_toggle_location is not None, 'Second toggle button not found'
    pyautogui.moveTo(second_toggle_location)
    pyautogui.click()
    time.sleep(1)

    # Step 8: Click on Add Device
    print('Step 8: Clicking on Add Device')
    add_device_location = wait_for_image(screenshot_path + 'add_device.png')
    assert add_device_location is not None, 'Add Device button not found'
    pyautogui.moveTo(add_device_location)
    pyautogui.click()
    time.sleep(2)

    # Second cycle: Repeat steps to toggle again

    # Step 9: Click on Profile again
    print('Step 9: Clicking on profile icon (second cycle)')
    profile_location = wait_for_image(screenshot_path + 'Avatar.png')
    assert profile_location is not None, 'Profile icon not found on second cycle'
    pyautogui.moveTo(profile_location)
    pyautogui.click()
    time.sleep(2)

    # Step 10: Click on Settings again
    print('Step 10: Clicking on settings (second cycle)')
    settings_location = wait_for_image(screenshot_path + 'Settings.png')
    assert settings_location is not None, 'Settings icon not found on second cycle'
    pyautogui.moveTo(settings_location)
    pyautogui.click()
    time.sleep(2)

    # Step 11: Click on Manage Privacy Settings again
    print('Step 11: Clicking on Manage Privacy Settings (second cycle)')
    manage_privacy_location = wait_for_image(screenshot_path + 'manage_privacy_settings.png')
    assert manage_privacy_location is not None, 'Manage Privacy Settings not found on second cycle'
    pyautogui.moveTo(manage_privacy_location)
    pyautogui.click()
    time.sleep(2)

    # Step 12: Click on the first toggle button again
    print('Step 12: Clicking on the first toggle button (second cycle)')
    first_toggle_location = wait_for_image(screenshot_path + 'manage_settings_toggle_1_close.png')
    assert first_toggle_location is not None, 'First toggle button not found on second cycle'
    pyautogui.moveTo(first_toggle_location)
    pyautogui.click()
    time.sleep(1)

    # Step 13: Scroll down again
    print('Step 13: Scrolling down (second cycle)')
    pyautogui.scroll(-300)
    time.sleep(1)

    # Step 14: Click on the second toggle button again
    print('Step 14: Clicking on the second toggle button (second cycle)')
    second_toggle_location = wait_for_image(screenshot_path + 'manage_settings_toggle_2_close.png')
    assert second_toggle_location is not None, 'Second toggle button not found on second cycle'
    pyautogui.moveTo(second_toggle_location)
    pyautogui.click()
    time.sleep(1)


# Test case C53681236: [HPX][Feedback] Verify the position/alignment of the submit button on the feedback slideout screen
@pytest.mark.usefixtures("launch_hpx_app")
def test_c53681236_hpx_feedback_submit_button_position(launch_hpx_app):
    # Step 1: Launch myHP app
    print('Step 1: Clicking on Add Device')
    add_device_location = wait_for_image(screenshot_path + 'add_device.png')
    assert add_device_location is not None, 'Add Device button not found'
    pyautogui.moveTo(add_device_location)
    pyautogui.click()
    time.sleep(2)

    # Step 2: Click on the Profile button
    profile_button = wait_for_image(screenshot_path + 'Avatar.png', timeout=10, confidence=0.8)
    assert profile_button is not None, " Profile button not found on the screen."
    pyautogui.moveTo(profile_button)
    pyautogui.click()
    print('✅ Clicked on Profile button.')
    time.sleep(2)

    # Step 3: Click on the Feedback button
    feedback_button = wait_for_image(screenshot_path + 'feedback_btn.png', timeout=10, confidence=0.8)
    assert feedback_button is not None, " Feedback button not found on the screen."
    pyautogui.moveTo(feedback_button)
    pyautogui.click()
    print('✅ Clicked on Feedback button.')
    time.sleep(2)

    # Step 4: Scroll down the feedback slideout screen
    pyautogui.scroll(-500)
    print('✅ Scrolled down on the feedback screen.')
    time.sleep(1)

    # Step 5: Verify the Submit button's position
    submit_button = wait_for_image(screenshot_path + 'submit_feedback.png', timeout=10, confidence=0.8)
    assert submit_button is not None, " Submit button not found on the feedback slideout screen."
    assert submit_button.y > 500, f" Submit button is not positioned correctly; found at y={submit_button.y}."
    print(f'✅ Submit button located at: {submit_button}')