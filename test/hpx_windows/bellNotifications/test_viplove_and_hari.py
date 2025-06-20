import time
import pyautogui
import subprocess
import pytest
import pygetwindow as gw
import logging

logger = logging.getLogger(__name__)

# Constants
screenshot_path = "screenshot/viplove_dark_mode/"
username = 'viplove.bisen@gmail.com'
password = 'Vippy@1234'

def wait_for_image(image, timeout=20, confidence=0.6):
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
    close_btn = pyautogui.locateCenterOnScreen(screenshot_path + "close_btn.png", confidence=0.7)
    pyautogui.moveTo(close_btn)
    pyautogui.click()
    time.sleep(2)
    
@pytest.fixture(scope='module')
def launch_hpx_app():
    logger.info("launching the app")
    app_id = "AD2F1837.myHP_v10z8vjag6ke6!App"
    subprocess.Popen(f'explorer shell:AppsFolder\\{app_id}', shell=True)
    time.sleep(3)
    yield
    # optional teardown
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

def login_hp_account():
    logger.info("login to hp account")
    if not activate_chrome_window():
        return
    time.sleep(10)  # Wait for page to fully load  
    username_or_email_address_textbox = wait_for_image(screenshot_path + "username_or_email_address_textbox.png")
    assert username_or_email_address_textbox is not None, "username_or_email_address_textbox not found"
    pyautogui.click(username_or_email_address_textbox) 
    pyautogui.write(username)
    pyautogui.press('tab',2) # Press tab twice to navigate to password field
    pyautogui.press('enter')
    time.sleep(5) 
    passwword_text_box = wait_for_image(screenshot_path + "passwword_text_box.png")
    assert passwword_text_box is not None, "passwword_text_box not found"
    pyautogui.click(passwword_text_box) 
    pyautogui.write(password,interval=0.1)  # Type password with a slight delay
    pyautogui.press('tab',2) 
    pyautogui.press('enter')   # Submit
    time.sleep(10) #wait for sign in to complete

def logout_hp_account(): 
    logger.info("log out to hp account")
    initials = wait_for_image(screenshot_path + "user_initials.png")
    pyautogui.click(initials)
    time.sleep(4)
    settings = wait_for_image(screenshot_path + "settings.png")
    pyautogui.click(settings)
    time.sleep(4)
    pyautogui.scroll(-500)
    sign_out_btn = wait_for_image(screenshot_path + "signout_button.png")
    assert sign_out_btn is not None, "Sign-out button not found"
    pyautogui.click(sign_out_btn)
    time.sleep(8)
    
# Test case 1
def test_tc_1_bell_notifications_global_header_navigation_visible_on_device_list_screen(launch_hpx_app):
    nav = wait_for_image(screenshot_path + "global_header_navigation.png")
    assert nav is not None, "Global Header Navigation not visible on device list screen"

# Test case 2
def test_tc_2_bell_notifications_global_header_navigation_includes_bell_icon(launch_hpx_app):
    bell_icon = wait_for_image(screenshot_path + "bell_icon.png")
    assert bell_icon is not None, "Bell Icon not found in Global Header Navigation"

# Test case 3
def test_tc_3_bell_notifications_bell_icon_can_be_clicked(launch_hpx_app):
    bell_icon = wait_for_image(screenshot_path + "bell_icon.png")
    assert bell_icon is not None, "Bell icon not found!"
    pyautogui.moveTo(bell_icon)
    pyautogui.click()
    time.sleep(3)
    click_on_close_button()

# Test case 4
def test_tc_4_bell_notifications_notifications_side_panel_opens_on_bell_click(launch_hpx_app):
    bell_icon = wait_for_image(screenshot_path + "bell_icon.png")
    assert bell_icon is not None, "Bell icon not found!"
    pyautogui.click(bell_icon)
    time.sleep(3)
    side_panel = wait_for_image(screenshot_path + "notifications_side_panel.png")
    assert side_panel is not None, "Notifications side panel did not open"
    click_on_close_button()

# Test case 5
def test_tc_5_bell_notifications_empty_bell_state_user_not_logged_in(launch_hpx_app):
    empty_bell = wait_for_image(screenshot_path + "empty_bell_icon.png")
    assert empty_bell is not None, "Empty bell state not shown when user is not logged in"

# Test case 6
def test_tc_6_bell_notifications_no_notifications_on_bell_click_user_not_logged_in(launch_hpx_app):
    bell_icon = wait_for_image(screenshot_path + "empty_bell_icon.png")
    assert bell_icon is not None, "Empty bell icon not found!"
    time.sleep(3)
    pyautogui.click(bell_icon)
    time.sleep(3)
    no_notifs = wait_for_image(screenshot_path + "no_notifications_message.png")
    assert no_notifs is not None, "Notifications shown when user is not logged in"
    click_on_close_button()

# Test case 7
def test_tc_7_bell_notifications_color_of_badging_on_bell_icon(launch_hpx_app):
    badge = wait_for_image(screenshot_path + "bell_badge_color.png")
    assert badge is not None, "Bell badge color is incorrect or badge missing"

# Test case 8
def test_tc_8_bell_notifications_transition_empty_to_notification_bell_on_login(launch_hpx_app):
    empty_bell = wait_for_image(screenshot_path + "empty_bell_icon.png")
    assert empty_bell is not None, "Empty bell icon missing before login"
    # Assume login steps here or call login helper
    # After login:
    time.sleep(3)
    notif_bell = wait_for_image(screenshot_path + "notification_bell_icon.png")
    assert notif_bell is not None, "Bell did not transition to notification bell after login"

# Test case 9
def test_tc_9_bell_notifications_device_list_blurs_when_nav_side_panel_opened(launch_hpx_app):
    bell_icon = wait_for_image(screenshot_path + "bell_icon.png")
    pyautogui.click(bell_icon)
    time.sleep(3)
    blurred_bg = wait_for_image(screenshot_path + "device_list_blurred.png")
    assert blurred_bg is not None, "Device list page not blurred when side panel opened"
    click_on_close_button()

# Test case 10
def test_tc_10_bell_notifications_back_button_visible_on_nav_side_panel(launch_hpx_app):
    bell_icon = wait_for_image(screenshot_path + "bell_icon.png")
    pyautogui.click(bell_icon)
    back_btn = wait_for_image(screenshot_path + "close_btn.png")
    assert back_btn is not None, "Back button not visible on Navigation side panel"
    click_on_close_button()

# Test case 11
def test_tc_11_bell_notifications_back_button_named_close_can_be_clicked(launch_hpx_app):
    bell_icon = wait_for_image(screenshot_path + "bell_icon.png")
    pyautogui.click(bell_icon)
    time.sleep(3)
    close_btn = wait_for_image(screenshot_path + "close_btn.png")
    assert close_btn is not None, "Close (Back) button not found"
    click_on_close_button()

# Test case 11
def test_tc_11_bell_notifications_back_button_named_close_can_be_clicked(launch_hpx_app):
    bell_icon = wait_for_image(screenshot_path + "bell_icon.png")
    pyautogui.click(bell_icon)
    time.sleep(3)
    close_btn = wait_for_image(screenshot_path + "close_btn.png")
    assert close_btn is not None, "Close (Back) button not found"
    click_on_close_button()
    
    
# Test case 12
def test_tc_12_bell_notifications_user_initials_visible_after_sign_in(launch_hpx_app):
    initials = wait_for_image(screenshot_path + "user_initials.png")
    assert initials is not None, "User initials not visible after sign-in"

# Test case 13
def test_tc_13_bell_notifications_user_can_click_initials_on_global_nav_panel(launch_hpx_app):
    initials = wait_for_image(screenshot_path + "user_initials.png")
    assert initials is not None, "User initials not found"
    pyautogui.click(initials)
    click_on_close_button()
    
    # Test case 14
def test_tc_14_bell_notifications_global_side_panel_opens_on_initials_click(launch_hpx_app):
    initials = wait_for_image(screenshot_path + "user_initials.png")
    pyautogui.click(initials)
    time.sleep(2)
    side_panel = wait_for_image(screenshot_path + "global_side_panel.png")
    assert side_panel is not None, "Global side panel did not open on initials click"
    click_on_close_button()

# Test case 15 Should not run it for time being may be keep this at the end as it wil sign out application
#@pytest.mark.skip(reason="This test is will sign out the application, skipping for now")
def test_tc_15_bell_notifications_user_can_sign_out_successfully(launch_hpx_app):
    logout_hp_account()
    # Verify sign-out by checking sign-in button visible again
    sign_in_btn = wait_for_image(screenshot_path + "signin_button.png")
    assert sign_in_btn is not None, "Sign-in button not visible after sign-out"

# Test case 16 Should not run it for time being may be keep this at the  end as it wil sign out application
@pytest.mark.skip(reason="This test should only be executed confirming sign-in functionality, skipping for now")
def test_tc_16_bell_notifications_login_using_sign_in_option_in_bell_flyout(launch_hpx_app):
    sign_in_option = wait_for_image(screenshot_path + "signin_button.png")
    assert sign_in_option is not None, "Sign-in option not found in Bell Flyout"
    pyautogui.click(sign_in_option) 
    activate_chrome_window()
    login_hp_account()
    

# Test case 17 Should not run it for time being may be keep this at the  end as it wil sign out application
#@pytest.mark.skip(reason="This test should only be executed confirming sign-in functionality, skipping for now")
def test_tc_17_bell_notifications_create_account_using_sign_in_create_account_option_in_bell_flyout(launch_hpx_app):
    time.sleep(3)
    bell_icon = wait_for_image(screenshot_path + "bell_icon_sign_in.png")
    pyautogui.click(bell_icon)
    time.sleep(3)
    create_account_option = wait_for_image(screenshot_path + "create_account_option_bell_flyout.png")
    assert create_account_option is not None, "Create account option not found in Bell Flyout"
    pyautogui.click(create_account_option)
    activate_chrome_window()
    login_hp_account()
    
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