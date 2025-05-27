import time
import pyautogui
import subprocess
import pytest

screenshot_path = "screenshot/"

def wait_for_image(image, timeout=10, confidence=0.8):
    start_time = time.time()
    while True:
        location = pyautogui.locateCenterOnScreen(image, confidence=confidence)
        if location:
            return location
        if time.time() - start_time > timeout:
            return None
        time.sleep(1)
        
def click_on_close_button():
    time.sleep(5)
    close_btn = pyautogui.locateCenterOnScreen(screenshot_path + "close_btn.png", confidence=0.7)
    pyautogui.moveTo(close_btn)
    pyautogui.click()
    time.sleep(2)

@pytest.fixture(scope='module')
def launch_hpx_app():
    app_id = "AD2F1837.myHP_v10z8vjag6ke6!App"
    subprocess.Popen(f'explorer shell:AppsFolder\\{app_id}', shell=True)
    time.sleep(5)
    yield
    # optional teardown


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
    side_panel = wait_for_image(screenshot_path + "global_side_panel.png")
    assert side_panel is not None, "Global side panel did not open on initials click"
    click_on_close_button()

# Test case 15 Should not run it for time being may be keep this at the  end as it wil sign out application
def test_tc_15_bell_notifications_user_can_sign_out_successfully(launch_hpx_app):
    sign_out_btn = wait_for_image(screenshot_path + "signout_button.png")
    assert sign_out_btn is not None, "Sign-out button not found"
    pyautogui.click(sign_out_btn)
    time.sleep(3)
    # Verify sign-out by checking sign-in button visible again
    sign_in_btn = wait_for_image(screenshot_path + "signin_button.png")
    assert sign_in_btn is not None, "Sign-in button not visible after sign-out"

# Test case 16 Should not run it for time being may be keep this at the  end as it wil sign out application
def test_tc_16_bell_notifications_login_using_sign_in_option_in_bell_flyout(launch_hpx_app):
    bell_icon = wait_for_image(screenshot_path + "bell_icon.png")
    pyautogui.click(bell_icon)
    sign_in_option = wait_for_image(screenshot_path + "signin_option_bell_flyout.png")
    assert sign_in_option is not None, "Sign-in option not found in Bell Flyout"
    pyautogui.click(sign_in_option)
    time.sleep(5)

# Test case 17 Should not run it for time being may be keep this at the  end as it wil sign out application
def test_tc_17_bell_notifications_create_account_using_sign_in_create_account_option_in_bell_flyout(launch_hpx_app):
    bell_icon = wait_for_image(screenshot_path + "bell_icon.png")
    pyautogui.click(bell_icon)
    create_account_option = wait_for_image(screenshot_path + "create_account_option_bell_flyout.png")
    assert create_account_option is not None, "Create account option not found in Bell Flyout"
    pyautogui.click(create_account_option)
    time.sleep(5)

# Test case 18
def test_tc_18_application_privacy_validate_common_consents_screen_accessibility(launch_hpx_app):
    consents_screen = wait_for_image(screenshot_path + "common_consents_screen.png")
    assert consents_screen is not None, "App and Device Common Consents screen not accessible"

# Test case 19
def test_tc_19_application_privacy_validate_common_consents_screen_accessibility_duplicate(launch_hpx_app):
    consents_screen = wait_for_image(screenshot_path + "common_consents_screen.png")
    assert consents_screen is not None, "App and Device Common Consents screen not accessible (duplicate test)"

# Test case 20
def test_tc_20_application_privacy_buttons_layout_manage_choices_row(launch_hpx_app):
    buttons_layout = wait_for_image(screenshot_path + "manage_choices_buttons_row.png")
    assert buttons_layout is not None, "Buttons layout incorrect on Manage choices page for ROW"

if __name__ == '__main__':
    pytest.main([__file__])