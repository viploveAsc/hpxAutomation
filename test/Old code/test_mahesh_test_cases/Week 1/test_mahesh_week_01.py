import time
import pyautogui
import subprocess
import pytest
import pygetwindow as gw
import logging

logger = logging.getLogger(__name__)

# Constants
screenshot_path = "screenshot/mahesh_dark_mode/"



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
    time.sleep(2)
    logger.info("Clicking close button")
    close_btn = pyautogui.locateCenterOnScreen("close_btn.png", confidence=0.7)
    pyautogui.moveTo(close_btn)
    pyautogui.click()
    time.sleep(2)

def relaunch_hpx_app():
    logger.info("Relaunching the app")
    app_id = "AD2F1837.myHP_v10z8vjag6ke6!App"
    subprocess.Popen(f'explorer shell:AppsFolder\\{app_id}', shell=True)
    time.sleep(30)  # Allow enough time for the app to launch


@pytest.fixture(scope='function')
def launch_hpx_app():
    app_id = "AD2F1837.myHP_v10z8vjag6ke6!App"

    print("Launching HPX App...")
    subprocess.Popen(f'explorer shell:AppsFolder\\{app_id}', shell=True)
    time.sleep(30)
    yield True

    # --- Teardown Logic using subprocess ---
    print("Closing HPX App...")
    try:
        # Replace with the actual process name of your app
        subprocess.run(["taskkill", "/f", "/im", "HP.myHP.exe"], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except subprocess.CalledProcessError:
        print("Warning: HPX App might already be closed or not found.")



def activate_chrome_window():
    # Wait for Chrome to open and detect the correct window
    logger.info("activating chrome window")
    for _ in range(10):
        windows = gw.getWindowsWithTitle('HP account')
        if windows:
            chrome_window = windows[0]
            chrome_window.activate()
            return True
        time.sleep(1)
    print("Chrome window not found.")
    return False

# Test case C53304022
#App-only Consents screen is shown during First use Flow
def test_tc_C53304022_(launch_hpx_app):

    home_indicator = wait_for_image(screenshot_path + "consent_scrn_txt.png", timeout=10, confidence=0.8)
    assert home_indicator, "Home screen not detected; app launch may have failed."
    print("Successfully launched MyHP app.")

# Test case C53304061
#app_and_device_common_consents_are_displayed
def test_tc_C53304061_(launch_hpx_app):

    home_indicator = wait_for_image(screenshot_path + "consent_scrn_txt.png", timeout=10, confidence=0.8)
    assert home_indicator, "Home screen not detected; app launch may have failed."
    print("Successfully launched MyHP app.")

# Test case C53304064
#verify_strictly_necessary_notice_on_first_use
def test_tc_C53304064_(launch_hpx_app):

    home_indicator = wait_for_image(screenshot_path + "hp_btn.png", timeout=10, confidence=0.8)
    assert home_indicator, "Home screen not detected; app launch may have failed."
    print("Successfully launched MyHP app.")

    # Step 2: Verify strictly necessary notice on App and Device Common Consents screen
    privacypage_txt = wait_for_image(screenshot_path + "consent_scrn_txt.png", timeout=10, confidence=0.8)
    assert privacypage_txt, "text not detected; verification failed."
    print("Successfully Verified the Text")

# Test case C53304068
#verify_back_button_layout_on_manage_choices_page
def test_tc_C53304068_(launch_hpx_app):

    home_indicator = wait_for_image(screenshot_path + "hp_btn.png", timeout=10, confidence=0.8)
    assert home_indicator, "Home screen not detected; app launch may have failed."
    print("Successfully launched MyHP app.")

    time.sleep(5)
    pyautogui.scroll(-1000)
    time.sleep(5)
    manage_options_btn = wait_for_image(screenshot_path + "Manage_choices.png", timeout=10, confidence=0.8)
    assert manage_options_btn, "'Manage options' button not found."
    pyautogui.moveTo(manage_options_btn)
    pyautogui.click()
    time.sleep(5)

    manage_page_indicator = wait_for_image(screenshot_path + "privacy_page.png", timeout=10, confidence=0.8)
    assert manage_page_indicator, "Manage options page failed to load."
    print("verification successfull Manage options.")

    time.sleep(5)
    pyautogui.scroll(-1000)
    time.sleep(3)
    back_btn = wait_for_image(screenshot_path + "back_btn.png", timeout=10, confidence=0.8)
    assert back_btn, "'Back' button not found."
    pyautogui.moveTo(back_btn)
    pyautogui.click()
    time.sleep(5)

    home_indicator_after = wait_for_image(screenshot_path + "privacy_page.png", timeout=10)
    assert home_indicator_after, "Failed to return to home screen after 'Back' button click."
    print("Home screen")

# Test case C53304066
#verify_manage_options_button_layout
def test_tc_C53304066_(launch_hpx_app):

    home_indicator = wait_for_image(screenshot_path + "hp_btn.png", timeout=10, confidence=0.8)
    assert home_indicator, "Home screen not detected; app launch may have failed."
    print("Successfully launched MyHP app.")

    time.sleep(5)
    pyautogui.scroll(-1000)
    time.sleep(5)
    manage_options_btn = wait_for_image(screenshot_path + "Manage_choices.png", timeout=10, confidence=0.8)
    assert manage_options_btn, "'Manage options' button not found."
    pyautogui.moveTo(manage_options_btn)
    pyautogui.click()
    time.sleep(5)

    manage_page_indicator = wait_for_image(screenshot_path + "privacy_page.png", timeout=10, confidence=0.8)
    assert manage_page_indicator, "Manage options page failed to load."
    print("verification successfull Manage options.")

# Test case C53304067
#verify_manage_choices_page_content
def test_tc_C53304067_(launch_hpx_app):

    home_indicator = wait_for_image(screenshot_path + "hp_btn.png", timeout=10, confidence=0.8)
    assert home_indicator, "Home screen not detected; app launch may have failed."
    time.sleep(5)
    pyautogui.scroll(-1000)
    time.sleep(5)

    manage_options_btn = wait_for_image(screenshot_path + "Manage_choices.png", timeout=10, confidence=0.8)
    assert manage_options_btn is not None, "'Manage options' button not found."
    pyautogui.click(manage_options_btn)
    time.sleep(2)

    manage_choices_page = wait_for_image(screenshot_path + "privacy_page.png", timeout=10, confidence=0.8)
    assert manage_choices_page is not None, "'Manage choices' page did not load successfully."

    manage_choices_content = wait_for_image(screenshot_path + "consent_scrn_txt.png", timeout=10, confidence=0.8)
    assert manage_choices_content is not None, "'Manage choices' page content not displayed."

    ui_elements = wait_for_image(screenshot_path + "manage_choices_toggle.png", timeout=10, confidence=0.8)
    assert ui_elements is not None, "Expected UI elements on 'Manage choices' page not displayed."

# Test case C53304065
#verify_app_and_device_common_consents_screen_content
def test_tc_C53304065_(launch_hpx_app):

    launch_screen = wait_for_image(screenshot_path + "hp_btn.png", timeout=10, confidence=0.8)
    assert launch_screen is not None, "Launch screen not displayed."

    common_consents_content = wait_for_image(screenshot_path + "consent_scrn_txt.png", timeout=10, confidence=0.8)
    assert common_consents_content is not None, "Common Consents Privacy screen not displayed."

    #hp_logo = wait_for_image("hp_logo.png", timeout=10, confidence=0.8)
    #assert hp_logo is not None, "HP logo not displayed on Common Consents screen."

    privacy_heading = wait_for_image(screenshot_path + "privacy_page.png", timeout=10, confidence=0.8)
    assert privacy_heading is not None, "Privacy heading not displayed as expected."

    app_privacy_tile = wait_for_image(screenshot_path + "app_consentpage.png", timeout=10, confidence=0.8)
    assert app_privacy_tile is not None, "App Privacy tile not present."

    #computer_privacy_tile = wait_for_image("computer_privacy_tile.png", timeout=10, confidence=0.8)
    #assert computer_privacy_tile is not None, "Computer Privacy tile not present."

    #body_text = wait_for_image("body_text.png", timeout=10, confidence=0.8)
    #assert body_text is not None, "Body text not displayed on Common Consents screen."

    #links = wait_for_image("links.png", timeout=10, confidence=0.8)
   # assert links is not None, "Not all links redirect to the respective pages."


# Test case C53304023
#App-only Consents screen is shown on re-launch if App Consents are not set yet.
def test_tc_C53304023_(launch_hpx_app):

    home_indicator = wait_for_image(screenshot_path + "consent_scrn_txt.png", timeout=10, confidence=0.8)
    assert home_indicator, "Home screen not detected; app launch may have failed."
    print("Successfully launched MyHP app.")

    time.sleep(5)
    pyautogui.scroll(-1000)
    time.sleep(5)
    manage_options_btn = wait_for_image(screenshot_path + "Manage_choices.png", timeout=10, confidence=0.8)
    assert manage_options_btn, "'Manage options' button not found."
    pyautogui.moveTo(manage_options_btn)
    pyautogui.click()
    time.sleep(5)  # Wait for the Manage Options page to load

    close_button_location = wait_for_image(screenshot_path + "x_btn.png", timeout=10, confidence=0.8)
    assert close_button_location is not None, "Close (X) button not found."
    pyautogui.moveTo(close_button_location)
    pyautogui.click()
    time.sleep(5)  # Allow time for the app to close

    relaunch_hpx_app()
    app_icon_location_relaunch = wait_for_image(screenshot_path + "consent_scrn_txt.png", timeout=10, confidence=0.8)
    assert app_icon_location_relaunch is not None, "MyHP app icon not found after relaunch."
    print("Test case executed successfully.")

# Test case C53304062
#app_and_device_common_consents_shown_on_relaunch_if_not_set
def test_tc_C53304062_(launch_hpx_app):

    home_indicator = wait_for_image(screenshot_path + "consent_scrn_txt.png", timeout=10, confidence=0.8)
    assert home_indicator, "Home screen not detected; app launch may have failed."
    print("Successfully launched MyHP app.")

    time.sleep(5)
    pyautogui.scroll(-1000)
    time.sleep(5)
    manage_options_btn = wait_for_image(screenshot_path + "Manage_choices.png", timeout=10, confidence=0.8)
    assert manage_options_btn, "'Manage options' button not found."
    pyautogui.moveTo(manage_options_btn)
    pyautogui.click()
    time.sleep(5)  # Wait for the Manage Options page to load

    close_button_location = wait_for_image(screenshot_path + "x_btn.png", timeout=10, confidence=0.8)
    assert close_button_location is not None, "Close (X) button not found."
    pyautogui.moveTo(close_button_location)
    pyautogui.click()
    time.sleep(5)  # Allow time for the app to close

    # Verify the app has closed
    # time.sleep(5)
    # app_icon_after_close = wait_for_image("hp_btn.png", timeout=10, confidence=0.8)
    # assert app_icon_after_close is None, "App did not close successfully."

    relaunch_hpx_app()
    app_icon_location_relaunch = wait_for_image(screenshot_path + "consent_scrn_txt.png", timeout=10, confidence=0.8)
    assert app_icon_location_relaunch is not None, "MyHP app icon not found after relaunch."

    print("Test case executed successfully.")

# Test case C53304027
#App-only Consents screen is displayed on the Unmanaged Device.
def test_tc_C53304027_(launch_hpx_app):

    home_indicator = wait_for_image(screenshot_path + "consent_scrn_txt.png", timeout=10, confidence=0.8)
    assert home_indicator, "Home screen not detected; app launch may have failed."
    print("Successfully launched MyHP app.")
    time.sleep(3)

# Test case C53304032
#Verify 'Manage Choices' button layout on the App-only Consents screen for the US.
def test_tc_C53304032_(launch_hpx_app):
    home_indicator = wait_for_image(screenshot_path + "consent_scrn_txt.png", timeout=10, confidence=0.8)
    assert home_indicator, "Home screen not detected; app launch may have failed."
    print("Successfully launched MyHP app.")

    time.sleep(5)
    pyautogui.scroll(-1000)
    time.sleep(5)
    manage_options_btn = wait_for_image(screenshot_path + "Manage_choices.png", timeout=10, confidence=0.8)
    assert manage_options_btn, "'Manage options' button not found."
    pyautogui.moveTo(manage_options_btn)
    pyautogui.click()
    time.sleep(5)

    manage_page_indicator = wait_for_image(screenshot_path + "privacy_page.png", timeout=10, confidence=0.8)
    assert manage_page_indicator, "Manage options page failed to load."
    print("verification successfull Manage options.")

# Test case C53304034
#Verify 'Manage Choices' button layout on the App-only Consents screen for the US.
def test_tc_C53304034_(launch_hpx_app):
    home_indicator = wait_for_image(screenshot_path + "consent_scrn_txt.png", timeout=10, confidence=0.8)
    assert home_indicator, "Home screen not detected; app launch may have failed."
    print("Successfully launched MyHP app.")

    time.sleep(5)
    pyautogui.scroll(-1000)
    time.sleep(5)
    manage_options_btn = wait_for_image(screenshot_path + "Manage_choices.png", timeout=10, confidence=0.8)
    assert manage_options_btn, "'Manage options' button not found."
    pyautogui.moveTo(manage_options_btn)
    pyautogui.click()
    time.sleep(5)

    manage_page_indicator = wait_for_image(screenshot_path + "privacy_page.png", timeout=10, confidence=0.8)
    assert manage_page_indicator, "Manage options page failed to load."
    print("verification successfull Manage options.")

    time.sleep(5)
    pyautogui.scroll(-1000)
    time.sleep(3)
    back_btn = wait_for_image(screenshot_path + "back_btn.png", timeout=10, confidence=0.8)
    assert back_btn, "'Back' button not found."
    pyautogui.moveTo(back_btn)
    pyautogui.click()
    time.sleep(5)

    home_indicator_after = wait_for_image(screenshot_path + "privacy_page.png", timeout=10)
    assert home_indicator_after, "Failed to return to home screen after 'Back' button click."
    print("Home screen")

# Test case C53304055
#verify_buttons_layout_on_app_only_consents_screen_for_row_repeat
def test_tc_C53304055_(launch_hpx_app):

    home_indicator = wait_for_image(screenshot_path + "consent_scrn_txt.png", timeout=10, confidence=0.8)
    assert home_indicator, "Home screen not detected; app launch may have failed."
    print("Successfully launched MyHP app.")
    time.sleep(3)
    pyautogui.scroll(-1000)
    time.sleep(3)

    accept_location = wait_for_image(screenshot_path + "Acccpt_btn.png", timeout=10, confidence=0.8)
    assert accept_location is not None, "'Accept All' button not found on screen."

    decline_location = wait_for_image(screenshot_path + "decline_btn.png", timeout=10, confidence=0.8)
    assert decline_location is not None, "'Decline Optional Data' button not found on screen."

    manage_location = wait_for_image(screenshot_path + "Manage_choices.png", timeout=10, confidence=0.8)
    assert manage_location is not None, "'Manage Options' button not found on screen."

    print("All privacy option buttons are visible on the app.")

# Test case C53304057
#verify_app_only_consents_manage_choices_content
def test_tc_C53304057_(launch_hpx_app):

    home_indicator = wait_for_image(screenshot_path + "consent_scrn_txt.png", timeout=10, confidence=0.8)
    assert home_indicator, "Home screen not detected; app launch may have failed."
    print("Successfully launched MyHP app.")

    time.sleep(5)
    pyautogui.scroll(-1000)
    time.sleep(5)
    manage_options_btn = wait_for_image(screenshot_path + "Manage_choices.png", timeout=10, confidence=0.8)
    assert manage_options_btn, "'Manage options' button not found."
    pyautogui.moveTo(manage_options_btn)
    pyautogui.click()
    time.sleep(5)

    #Verify manage choice page content

# Test case C53304059
#verify_buttons_layout_on_app_only_consents_screen_for_row
def test_tc_C53304059_(launch_hpx_app):

    home_indicator = wait_for_image(screenshot_path + "consent_scrn_txt.png", timeout=10, confidence=0.8)
    assert home_indicator, "Home screen not detected; app launch may have failed."
    print("Successfully launched MyHP app.")
    time.sleep(3)
    pyautogui.scroll(-1000)
    time.sleep(3)
    accept_location = wait_for_image(screenshot_path + "Acccpt_btn.png", timeout=10, confidence=0.8)
    assert accept_location is not None, "'Accept All' button not found on screen."

    decline_location = wait_for_image(screenshot_path + "decline_btn.png", timeout=10, confidence=0.8)
    assert decline_location is not None, "'Decline Optional Data' button not found on screen."

    manage_location = wait_for_image(screenshot_path + "Manage_choices.png", timeout=10, confidence=0.8)
    assert manage_location is not None, "'Manage Options' button not found on screen."

    print("All privacy option buttons are visible on the app.")



# Test case C53304073
#verify_continue_button_layout_on_the_app_and_device_common_consents_manage_choices_page_for_the_us
def test_tc_C53304073_(launch_hpx_app):

    launch_screen = wait_for_image(screenshot_path + "hp_btn.png", timeout=10, confidence=0.8)
    assert launch_screen is not None, "Launch screen not displayed for App and Device Common Consents."

    consents_screen = wait_for_image(screenshot_path + "consent_scrn_txt.png", timeout=10, confidence=0.8)
    assert consents_screen is not None, "App and Device Common Consents screen not displayed."
    time.sleep(3)
    pyautogui.scroll(-1000)
    time.sleep(3)
    manage_options_btn = wait_for_image(screenshot_path + "Manage_choices.png", timeout=10, confidence=0.8)
    assert manage_options_btn is not None, "'Manage options' button not found.'"
    pyautogui.click(manage_options_btn)
    time.sleep(2)

    manage_choices_screen = wait_for_image(screenshot_path + "privacy_page.png", timeout=10, confidence=0.8)
    assert manage_choices_screen is not None, "'Manage choices' page did not load successfully.'"
    time.sleep(2)
    pyautogui.scroll(-1000)
    time.sleep(2)
    continue_btn = wait_for_image(screenshot_path + "continue_btn.png", timeout=10, confidence=0.8)
    assert continue_btn is not None, "'Continue' button not found.'"
    pyautogui.click(continue_btn)
    time.sleep(2)
    registration_home = wait_for_image(screenshot_path + "bell_btn.png", timeout=10, confidence=0.8)
    assert registration_home is not None, "Registration/Home page did not load successfully."

# Test case C53304035
#verify_continue_button_layout_on_manage_choices_screen_for_us
@pytest.mark.skip(reason="This test should only be executed confirming sign-in functionality, skipping for now")
def test_tc_C53304035_(launch_hpx_app):

    home_indicator = wait_for_image(screenshot_path + "consent_scrn_txt.png", timeout=10, confidence=0.8)
    assert home_indicator, "Home screen not detected; app launch may have failed."
    print("Successfully launched MyHP app.")

    time.sleep(5)
    pyautogui.scroll(-1000)
    time.sleep(5)
    manage_options_btn = wait_for_image(screenshot_path + "Manage_choices.png", timeout=10, confidence=0.8)
    assert manage_options_btn, "'Manage options' button not found."
    pyautogui.moveTo(manage_options_btn)
    pyautogui.click()
    time.sleep(2)

    manage_page_indicator = wait_for_image(screenshot_path + "privacy_page.png", timeout=10, confidence=0.8)
    assert manage_page_indicator, "Manage options page failed to load."
    print("verification successfull Manage options.")

    time.sleep(2)
    pyautogui.scroll(-1000)
    time.sleep(2)
    continue_btn = wait_for_image(screenshot_path + "continue_btn.png", timeout=10, confidence=0.8)
    assert continue_btn, "'Continue' button not found.'"
    pyautogui.moveTo(continue_btn)
    pyautogui.click()
    time.sleep(5)

    home_page = wait_for_image(screenshot_path + "bell_btn", timeout=10, confidence=0.8)
    assert home_page, "Failed to reach the home page."
    print("Home screen")

# Test case C53304031
#Verify 'Decline optional data' Button layout on the App-only Consents screen for the US.
@pytest.mark.skip(reason="This test should only be executed confirming sign-in functionality, skipping for now")
def test_tc_C53304031_(launch_hpx_app):

    home_indicator = wait_for_image(screenshot_path + "consent_scrn_txt.png", timeout=10, confidence=0.8)
    assert home_indicator, "Home screen not detected; app launch may have failed."
    print("Successfully launched MyHP app.")

    time.sleep(5)
    pyautogui.scroll(-1000)
    time.sleep(5)

    DeclineOpt_btn_options_btn = wait_for_image(screenshot_path + "decline_btn.png", timeout=10, confidence=0.8)
    assert DeclineOpt_btn_options_btn, "'Decline optional data' button not found."
    pyautogui.moveTo(DeclineOpt_btn_options_btn)
    pyautogui.click()
    time.sleep(5)

# Test case C53304030
#Verify 'Accept All' button layout on the App-only Consents screen for the US.
@pytest.mark.skip(reason="This test should only be executed confirming sign-in functionality, skipping for now")
def test_tc_C53304030_(launch_hpx_app):

    home_indicator = wait_for_image(screenshot_path + "consent_scrn_txt.png", timeout=10, confidence=0.8)
    assert home_indicator, "Home screen not detected; app launch may have failed."
    print("Successfully launched MyHP app.")

    time.sleep(5)
    pyautogui.scroll(-1000)
    time.sleep(5)
    Accept_Option_btn = wait_for_image(screenshot_path + "Acccpt_btn.png", timeout=10, confidence=0.8)
    assert Accept_Option_btn, "Accept All options' button not found."
    pyautogui.moveTo(Accept_Option_btn)
    pyautogui.click()
    print("Test case executed successfully.")

# Test case C53304071
#app_and_device_common_consents_not_shown_if_consents_already_set
@pytest.mark.skip(reason="This test should only be executed confirming sign-in functionality, skipping for now")
def test_tc_C53304071_(launch_hpx_app):

    home_indicator = wait_for_image(screenshot_path + "hp_btn.png", timeout=10, confidence=0.8)
    assert home_indicator, "Home screen not detected; app launch may have failed."
    print("Successfully launched MyHP app.")

    time.sleep(5)
    pyautogui.scroll(-1000)
    time.sleep(5)
    Accept_options_btn = wait_for_image(screenshot_path + "Acccpt_btn.png", timeout=10, confidence=0.8)
    assert Accept_options_btn, "'Accept options' button not found."
    pyautogui.moveTo(Accept_options_btn)
    pyautogui.click()
    time.sleep(5)  # Wait for the Manage Options page to load

    close_button_location = wait_for_image(screenshot_path + "x_btn.png", timeout=10, confidence=0.8)
    assert close_button_location is not None, "Close (X) button not found."
    pyautogui.moveTo(close_button_location)
    pyautogui.click()
    time.sleep(5)  # Allow time for the app to close

    relaunch_hpx_app()
    app_icon_location_relaunch = wait_for_image(screenshot_path + "hp_btn.png", timeout=10, confidence=0.8)
    assert app_icon_location_relaunch is not None, "MyHP app icon not found after relaunch."

# Test case C53304069
#verify_decline_optional_data_button_layout
@pytest.mark.skip(reason="This test should only be executed confirming sign-in functionality, skipping for now")
def test_tc_C53304069_(launch_hpx_app):

    app_logo = wait_for_image(screenshot_path + "hp_btn.png", timeout=15, confidence=0.8)
    assert app_logo is not None, "App did not launch properly - app logo not found."

    time.sleep(5)
    pyautogui.scroll(-1000)
    time.sleep(5)
    button_location = wait_for_image(screenshot_path + "decline_btn.png", timeout=15, confidence=0.8)
    assert button_location is not None, "'Decline Optional Data' button not found on the screen."
    pyautogui.moveTo(button_location)
    pyautogui.click()
    time.sleep(3)  # Wait for any UI updates
    home_screen = pyautogui.locateCenterOnScreen(screenshot_path + "bell_btn.png", timeout=15, confidence=0.8)
    assert home_screen is None,("'Home Screen not detected, app launch may have failed.'")

# Test case C53304026
#App-only Consents screen is NOT displayed on the Managed device.
def test_tc_C53304026_(launch_hpx_app):

    home_indicator = wait_for_image(screenshot_path + "bell_btn.png", timeout=10, confidence=0.8)
    assert home_indicator, "Home screen not detected; app launch may have failed."
    print("Successfully launched MyHP app.")
    time.sleep(3)

# Test case C53304060
#app_privacy_common_consents_not_shown_on_managed_device
def test_tc_C53304060_(launch_hpx_app):
    home_indicator = wait_for_image(screenshot_path + "bell_btn.png", timeout=10, confidence=0.8)
    assert home_indicator, "Home screen not detected; app launch may have failed."
    print("Successfully launched MyHP app.")

# Test case C53304072
#app_and_device_common_consents_not_shown_if_consents_already_set
def test_tc_C53304072_(launch_hpx_app):

    home_indicator = wait_for_image(screenshot_path + "bell_btn.png", timeout=10, confidence=0.8)
    assert home_indicator, "Home screen not detected; app launch may have failed."
    print("Verification of App launched.")

if __name__ == '__main__':
    pytest.main([__file__])
