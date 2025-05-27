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
    time.sleep(5)
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
    time.sleep(5)
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


if __name__ == '__main__':
    pytest.main([__file__])