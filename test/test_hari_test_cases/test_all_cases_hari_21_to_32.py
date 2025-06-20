import time
import pyautogui
import subprocess
import pytest

screenshot_path = "screenshot/viplove_dark_mode/"

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


# Test case 21
@pytest.mark.skip(reason="This test should only be executed when user login first time to application")
def test_tc_21_application_privacy_accept_all_button_layout_us(launch_hpx_app):
    accept_all_btn = wait_for_image(screenshot_path + "accept_all_button_us.png")
    assert accept_all_btn is not None, "'Accept All' Button layout incorrect on Common Consents page for US"

# Test case 22
@pytest.mark.skip(reason="This test should only be executed when user login first time to application")
def test_tc_22_consents_dark_mode_applied_on_all_elements(launch_hpx_app):
    dark_mode = wait_for_image(screenshot_path + "dark_mode_elements.png")
    assert dark_mode is not None, "Dark Mode not properly applied on all elements"

# Test case 23
@pytest.mark.skip(reason="This test should only be executed when user login first time to application")
def test_tc_23_consents_common_consents_displayed_if_device_consents_not_set_first_launch(launch_hpx_app):
    common_consents = wait_for_image(screenshot_path + "common_consents_first_launch.png")
    assert common_consents is not None, "Common Consents not displayed if device consents not set on first launch"

# Test case 24
@pytest.mark.skip(reason="This test should only be executed when user login first time to application")
def test_tc_24_consents_common_consents_page_shown_on_relaunch_if_not_set(launch_hpx_app):
    common_consents = wait_for_image(screenshot_path + "common_consents_relaunch.png")
    assert common_consents is not None, "Common Consents page not shown on re-launch if consents not set"

# Test case 25
@pytest.mark.skip(reason="This test should only be executed when user login first time to application")
def test_tc_25_consents_common_consents_not_shown_on_managed_device(launch_hpx_app):
    common_consents = wait_for_image(screenshot_path + "common_consents_managed_device.png")
    assert common_consents is None, "Common Consents shown on Managed device when they should not be"

# Test case 26
@pytest.mark.skip(reason="This test should only be executed when user login first time to application")
def test_tc_26_consents_common_consents_privacy_screen_accessibility(launch_hpx_app):
    privacy_screen = wait_for_image(screenshot_path + "common_consents_privacy_screen.png")
    assert privacy_screen is not None, "Common Consents Privacy screen not accessible"

# Test case 27
@pytest.mark.skip(reason="This test should only be executed when user login first time to application")
def test_tc_27_consents_buttons_layout_for_row(launch_hpx_app):
    buttons_layout = wait_for_image(screenshot_path + "common_consents_buttons_row.png")
    assert buttons_layout is not None, "Buttons layout incorrect on Common Consents page for ROW"

# Test case 28
@pytest.mark.skip(reason="This test should only be executed when user login first time to application")
def test_tc_28_consents_decline_optional_data_button_layout_us(launch_hpx_app):
    decline_btn = wait_for_image(screenshot_path + "decline_optional_data_button_us.png")
    assert decline_btn is not None, "'Decline Optional Data' button layout incorrect on Common Consents page for US"

# Test case 29
@pytest.mark.skip(reason="This test should only be executed when user login first time to application")
def test_tc_29_consents_common_consents_not_shown_if_already_set(launch_hpx_app):
    common_consents = wait_for_image(screenshot_path + "common_consents_already_set.png")
    assert common_consents is None, "Common Consents shown even though consents are already set"

# Test case 30
@pytest.mark.skip(reason="This test should only be executed when user login first time to application")
def test_tc_30_consents_device_consents_not_displayed_if_already_set(launch_hpx_app):
    device_consents = wait_for_image(screenshot_path + "device_consents_already_set.png")
    assert device_consents is None, "Device Consents displayed even though already set"

# Test case 31
@pytest.mark.skip(reason="This test should only be executed when user login first time to application")
def test_tc_31_consents_continue_button_layout_manage_choices_us(launch_hpx_app):
    continue_btn = wait_for_image(screenshot_path + "continue_button_manage_choices_us.png")
    assert continue_btn is not None, "'Continue' button layout incorrect on Common Consents Manage choices page for US"

# Test case 32
@pytest.mark.skip(reason="This test should only be executed when user login first time to application")
def test_tc_32_consents_accept_all_button_layout_us(launch_hpx_app):
    accept_all_btn = wait_for_image(screenshot_path + "accept_all_button_us.png")
    assert accept_all_btn is not None, "'Accept All' Button layout incorrect on Common Consents page for US"

if __name__ == '__main__':
    pytest.main([__file__])