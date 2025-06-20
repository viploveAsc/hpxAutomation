import time
import pyautogui
import subprocess
import pytest
import pygetwindow as gw

screenshot_path = "screenshot/hari_dark_mode/"

def wait_for_image(image, timeout=10, confidence=0.6):
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
        

@pytest.fixture(scope='module')
def launch_hpx_app():
    app_id = "AD2F1837.myHP_v10z8vjag6ke6!App"
    subprocess.Popen(f'explorer shell:AppsFolder\\{app_id}', shell=True)
    time.sleep(5)
    yield
    # optional teardown

    
#Test case 18
@pytest.mark.skip(reason="This test should only be executed when user login first time to application")
def test_tc_18_application_privacy_validate_common_consents_screen_accessibility(launch_hpx_app):
    consents_screen = wait_for_image(screenshot_path + "common_consents_screen.png")
    assert consents_screen is not None, "App and Device Common Consents screen not accessible"

# Test case 19
@pytest.mark.skip(reason="This test should only be executed when user login first time to application")
def test_tc_19_application_privacy_validate_common_consents_screen_accessibility_duplicate(launch_hpx_app):
    consents_screen = wait_for_image(screenshot_path + "common_consents_screen.png")
    assert consents_screen is not None, "App and Device Common Consents screen not accessible (duplicate test)"

# Test case 20
@pytest.mark.skip(reason="This test should only be executed when user login first time to application")
def test_tc_20_application_privacy_buttons_layout_manage_choices_row(launch_hpx_app):
    buttons_layout = wait_for_image(screenshot_path + "manage_choices_buttons_row.png")
    assert buttons_layout is not None, "Buttons layout incorrect on Manage choices page for ROW"

# Test case 21
@pytest.mark.skip(reason="This test should only be executed when user login first time to application")
def test_tc_21_application_privacy_manage_choices_buttons_layout_row(launch_hpx_app):
    # Step 1: Launch the HPX app using the fixture
 
    pyautogui.scroll(-1000)  # Negative value scrolls down
    time.sleep(2)
 
    # Step 2: Wait for and click on the 'Manage choices' button
    manage_choices_btn = wait_for_image(screenshot_path + "manage_choices_button.png")
    assert manage_choices_btn is not None, "'Manage options' button not found on Common Consents Privacy screen"
    pyautogui.click(manage_choices_btn)
    time.sleep(2)
 
    # Step 3: Wait for the 'Manage choices' screen to load
    manage_choices_screen = wait_for_image(screenshot_path + "manage_choices_screen.png")
    assert manage_choices_screen is not None, "'Manage choices' screen did not load successfully"
    pyautogui.scroll(-1000)
    time.sleep(2)
 
    # Step 4: Verify that the 'Continue' button is visible
    continue_btn = wait_for_image(screenshot_path + "continue_button.png")
    assert continue_btn is not None, "'Continue' button layout is incorrect or not found"
 
    # Step 5: Verify that the 'Back' button is visible
    back_btn = wait_for_image(screenshot_path + "back_button.png")
    assert back_btn is not None, "'Back' button layout is incorrect or not found"
 
    # Final Step: Print success message
    print(" 'Manage choices' screen button layout verified successfully.")
 
 
# Test case 22
@pytest.mark.skip(reason="This test should only be executed when user login first time to application")
def test_tc_22_consents_dark_mode_applied_on_all_elements(launch_hpx_app):
    # Launch the app and check dark mode on screen
    dark_mode = wait_for_image(screenshot_path + "dark_mode_elements.png", timeout=10)
    assert dark_mode is not None, " Dark Mode not properly applied on all elements"
    print("Dark Mode is properly applied on all elements.")
 
# Test case 23
@pytest.mark.skip(reason="This test should only be executed when user login first time to application")
def test_tc_23_consents_common_consents_displayed_if_device_consents_not_set_first_launch(launch_hpx_app):
    # Step 1: Wait for Common Consents screen on first app launch
    common_consents = wait_for_image(screenshot_path + "common_consents_first_launch.png", timeout=10)
 
    # Step 2: Assert and log
    assert common_consents is not None, " Common Consents not displayed on first launch when device consents not set"
    print("Common Consents displayed on first launch as expected (device consents not set)")
 
 
# Test case 24
@pytest.mark.skip(reason="This test should only be executed when user login first time to application")
def test_tc_24_consents_common_consents_page_shown_on_relaunch_if_not_set(launch_hpx_app):
    # Step 1: Wait for Common Consents screen to appear on first launch
    common_consents = wait_for_image(screenshot_path + "common_consents_relaunch.png", timeout=10)
    assert common_consents is not None, " Common Consents screen not shown on first launch"
 
    # Step 2: Scroll down to reveal Manage options button
    pyautogui.scroll(-1000)
    time.sleep(2)
 
    # Step 3: Click the 'Manage options' button
    manage_btn = wait_for_image(screenshot_path + "manage_choices_screen.png", timeout=10)
    assert manage_btn is not None, " 'Manage options' button not found"
    pyautogui.click(manage_btn)
    time.sleep(3)
 
    # Step 4: Close the app using the 'X' (close) button without setting consents
    close_btn = wait_for_image(screenshot_path + "close_btn.png", timeout=10)
    assert close_btn is not None, " Close button not found to exit the app"
    pyautogui.click(close_btn)
    time.sleep(3)
 
    # Step 5: Relaunch the app
    app_id = "AD2F1837.myHP_v10z8vjag6ke6!App"
    subprocess.Popen(f'explorer shell:AppsFolder\\{app_id}', shell=True)
    time.sleep(7)
 
    # Step 6: Verify that Common Consents screen is still shown after re-launch
    common_consents_again = wait_for_image(screenshot_path + "common_consents_relaunch.png", timeout=10)
    assert common_consents_again is not None, " Common Consents screen not shown again after re-launch"
 
    # Final Step: Print success message
    print(" Common Consents screen re-appears on app re-launch when consents are not set")
 
# Test case 25
@pytest.mark.skip(reason="This test should only be executed when user login first time to application")
def test_tc_25_consents_common_consents_not_shown_on_managed_device(launch_hpx_app):
    # Step 1: Ensure Common Consents screen is NOT shown on managed device
    home_page = wait_for_image(screenshot_path + "home_page_marker.png", timeout=15)
    assert home_page is not None, "HPX Home page did not load on managed device"
 
    # Final step: Print success confirmation
    print("HPX home page loads successfully.")
 
 
# Test case 26
@pytest.mark.skip(reason="This test should only be executed when user login first time to application")
def test_tc_26_consents_common_consents_privacy_screen_accessibility(launch_hpx_app):
    # Step 1: Wait for the Common Consents Privacy screen to appear
    privacy_screen = wait_for_image(screenshot_path + "common_consents_privacy_screen.png", timeout=10)
    assert privacy_screen is not None, " Common Consents Privacy screen not accessible"
 
    # Step 2: Print success message
    print(" Common Consents Privacy screen is accessible and displayed correctly")
 
 
# Test case 27
@pytest.mark.skip(reason="This test should only be executed when user login first time to application")
def test_tc_27_consents_buttons_layout_for_row(launch_hpx_app):
    # Step 1: Verify Common Consents screen is displayed
    consents_screen = wait_for_image(screenshot_path + "common_consents_screen.png", timeout=10)
    assert consents_screen is not None, " Common Consents screen not displayed"
 
    # Step 2: Scroll down in case buttons are not visible immediately
    pyautogui.scroll(-1000)
    time.sleep(2)
 
    # Step 3: Check for buttons layout specific to ROW
    buttons_layout = wait_for_image(screenshot_path + "common_consents_buttons_row.png", timeout=10)
    assert buttons_layout is not None, " Buttons layout incorrect on Common Consents page for ROW"
 
    # Step 4: Print success message
    print(" Buttons layout verified on Common Consents page for ROW")
 
 
# Test case 28
@pytest.mark.skip(reason="This test should only be executed when user login first time to application")
def test_tc_28_consents_decline_optional_data_button_layout_us(launch_hpx_app):
    # Step 1: Verify Common Consents screen is displayed
    common_consents_screen = wait_for_image(screenshot_path + "common_consents_screen.png", timeout=10)
    assert common_consents_screen is not None, " Common Consents Privacy screen not displayed"
 
    # Step 2: Scroll down to reveal the 'Decline Optional Data' button
    pyautogui.scroll(-500)  # Adjust scroll value if needed
    time.sleep(2)
 
    # Step 3: Locate and click the 'Decline Optional Data' button
    decline_btn = wait_for_image(screenshot_path + "decline_optional_data_button_us.png", timeout=10)
    assert decline_btn is not None, " 'Decline Optional Data' button not found on Common Consents page (US)"
    pyautogui.click(decline_btn)
    time.sleep(5)
 
    # Step 4: Wait for the Registration/Home Page to load
    home_page_element = wait_for_image(screenshot_path + "home_page_marker.png", timeout=15)
    assert home_page_element is not None, " Home/Registration page did not load after declining optional data"
 
    # Step 5: Print success message
    print(" Home/Registration page loaded successfully after clicking 'Decline Optional Data'")
 
# Test case 29
@pytest.mark.skip(reason="This test should only be executed when user login first time to application")
def test_tc_29_consents_common_consents_not_shown_if_already_set(launch_hpx_app):
    # Step 1: Simulate setting consents
    any_consent_button = wait_for_image(screenshot_path + "accept_all_button_us.png", timeout=10)
    assert any_consent_button is not None, "Consent button not found on first launch"
    pyautogui.click(any_consent_button)
    time.sleep(5)  # Allow navigation to home/registration
 
    # Step 2: Close the app (click on 'X')
    close_btn = wait_for_image(screenshot_path + "close_btn.png", timeout=10)
    assert close_btn is not None, "Close button not found"
    pyautogui.click(close_btn)
    time.sleep(3)
 
    # Step 3: Re-launch the app
    app_id = "AD2F1837.myHP_v10z8vjag6ke6!App"
    subprocess.Popen(f'explorer shell:AppsFolder\\{app_id}', shell=True)
    time.sleep(6)  # Wait for app to fully relaunch
 
    # Step 4: Verify Common Consents screen is NOT shown
    common_consents = wait_for_image(screenshot_path + "common_consents_already_set.png", timeout=10)
    assert common_consents is None, "Common Consents shown even though consents are already set"
 
    print(" Common Consents screen not shown on relaunch — as expected")
 
# Test case 30
@pytest.mark.skip(reason="This test should only be executed when user login first time to application")
def test_tc_30_consents_device_consents_not_displayed_if_already_set(launch_hpx_app):
    # Attempt to locate the Device Consents screen
    device_consents = wait_for_image(screenshot_path + "device_consents_already_set.png", timeout=10)
   
    # Assert that the image is NOT found
    assert device_consents is None, " Device Consents are displayed even though they should already be set"
 
    print(" Device Consents screen not displayed as expected (already set)")
 
 
# Test case 31
@pytest.mark.skip(reason="This test should only be executed when user login first time to application")
def test_tc_31_consents_continue_button_layout_manage_choices_us(launch_hpx_app):
    # Step 1: Scroll down to find and click 'Manage choices'
    pyautogui.scroll(-500)
    time.sleep(2)
    manage_choices_btn = wait_for_image(screenshot_path + "manage_choices_button.png")
    assert manage_choices_btn is not None, "'Manage choices' button not found"
    pyautogui.click(manage_choices_btn)
    time.sleep(3)
    # Step 2: Scroll down to find and click 'Continue'
    pyautogui.scroll(-1000)
    time.sleep(2)
    continue_btn = wait_for_image(screenshot_path + "continue_button_manage_choices_us.png")
    assert continue_btn is not None, "'Continue' button layout incorrect on Manage choices page for US"
    pyautogui.click(continue_btn)
    time.sleep(5)
    # Step 3: Verify homepage loaded by checking a known UI element
    home_page_element = wait_for_image(screenshot_path + "home_page_marker.png", timeout=15)
    assert home_page_element is not None, "Home page did not load as expected"
    print("Home page loaded successfully")
 
# Test case 32
@pytest.mark.skip(reason="This test should only be executed when user login first time to application")
def test_tc_32_consents_accept_all_button_layout_us(launch_hpx_app):
    # Scroll up to bring 'Accept All' button into view
    pyautogui.scroll(-1000)
    time.sleep(2)
    accept_all_btn = wait_for_image(screenshot_path + "accept_all_button_us.png")
    assert accept_all_btn is not None, "'Accept All' Button layout incorrect on Common Consents page for US"
    pyautogui.click(accept_all_btn)
    time.sleep(5)  # Wait for the home page to load
    # Optional: Verify a known home page element to confirm load (replace image as needed)
    home_page_element = wait_for_image(screenshot_path + "home_page_marker.png", timeout=15)
    assert home_page_element is not None, "Home page did not load as expected"
    print("Home page loaded successfully")
    
    
if __name__ == '__main__':
    pytest.main([__file__])