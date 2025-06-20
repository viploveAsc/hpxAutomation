import pytest
import pyautogui
import subprocess
import time
import logging
import pygetwindow as gw

# ---------- Constants ----------
screenshot_path = "screenshot/hari_dark_mode/"
app_id = "AD2F1837.myHP_v10z8vjag6ke6!App"
confidence = 0.9
timeout = 20
window_title = "HP"
settings_image = screenshot_path + "settings_page.png"

# ---------- Logger Setup ----------
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# ---------- Utility Functions ----------
def launch_hpx_app():
    logger.info("Launching HPX app...")
    subprocess.Popen(f'explorer shell:AppsFolder\\{app_id}', shell=True)
    # Wait dynamically for home screen
    wait_for_image(screenshot_path + "Homescreen.png", timeout=30)

def close_hpx_app():
    logger.info("Closing HPX app...")
    for win in gw.getWindowsWithTitle(window_title):
        win.close()
        logger.info(" App closed.")
        return
    pyautogui.hotkey('alt', 'f4')
    time.sleep(2)

def wait_for_image(image, timeout=timeout, confidence=confidence):
    logger.info(f"Waiting for image: {image}")
    start_time = time.time()
    while time.time() - start_time < timeout:
        location = pyautogui.locateCenterOnScreen(image, confidence=confidence)
        if location:
            return location
        time.sleep(1)
    logger.error(f"[TIMEOUT] Image not found: {image}")
    raise AssertionError(f"[TIMEOUT] Image not found: {image}")

def wait_and_click(image, timeout=timeout, confidence=confidence):
    location = wait_for_image(image, timeout, confidence)
    if location:
        pyautogui.click(location)
        time.sleep(2)
        return True
    return False

def click_image(image):
    location = wait_for_image(image)
    pyautogui.click(location)
    time.sleep(2)

def enter_text(image, text, tab_after=False):
    field = wait_for_image(image)
    pyautogui.click(field)
    pyautogui.write(text, interval=0.1)
    if tab_after:
        pyautogui.press('tab')
    time.sleep(1)

def clear_and_type(image, text):
    field = wait_for_image(image)
    pyautogui.click(field)
    pyautogui.hotkey("ctrl", "a")
    pyautogui.press("backspace")
    pyautogui.write(text, interval=0.1)
    time.sleep(1)

def scroll_privacy_screen(image):
    logger.info("Scrolling to show 'Accept All' button")
    location = wait_for_image(image)
    pyautogui.moveTo(location)
    pyautogui.scroll(-500)
    time.sleep(2)

def is_windows_notifications_enabled():
    on_toggle = screenshot_path + "windows_hp_notification_toggle_on.png"
    try:
        wait_for_image(on_toggle, timeout=5)
        return True
    except AssertionError:
        return False

def open_run_command_and_enter_uri(uri="hpx://settings"):
    logger.info(f"Opening Run dialog and launching URI: {uri}")
    pyautogui.hotkey('win', 'r')
    time.sleep(2)
    pyautogui.write(uri, interval=0.05)
    pyautogui.press('enter')
    time.sleep(15)

#C53304248-ITG
@pytest.mark.device_navigation
def test_tc_003_notification_section_and_device_status_visible():
    launch_hpx_app()
    wait_for_image(screenshot_path + "device_list.png")
    click_image(screenshot_path + "profile_icon.png")
    click_image(screenshot_path + "settings.png")
    assert wait_for_image(screenshot_path + "notification_section.png")
    close_hpx_app()
#C58755891-ITG
@pytest.mark.settings
def test_tc_002_toggle_state_persistence():
    launch_hpx_app()
    click_image(screenshot_path + "profile_icon.png")
    click_image(screenshot_path + "settings.png")
    click_image(screenshot_path + "device_supply_toggle_on.png")
    click_image(screenshot_path + "back_menu.png")
    click_image(screenshot_path + "close1.png")
    close_hpx_app()

    launch_hpx_app()
    click_image(screenshot_path + "profile_icon.png")
    click_image(screenshot_path + "settings.png")
    assert wait_for_image(screenshot_path + "device_supply_toggle_off.png"), "Toggle state not retained"
    close_hpx_app()
#C53304253-ITG
@pytest.mark.windows_dependency
def test_device_toggle_updates_when_windows_notifications_disabled():
    logger.info("Step 1: Launch HPX and verify toggle is initially ON")
    launch_hpx_app()
    click_image(screenshot_path + "profile_icon.png")
    click_image(screenshot_path + "settings.png")
    assert wait_for_image(screenshot_path + "device_supply_toggle_on.png"), " Initial toggle ON not found"
    close_hpx_app()

    logger.info("Step 2: Open Windows Notification Settings")
    subprocess.Popen("start ms-settings:notifications", shell=True)
    time.sleep(5)

    logger.info("Step 3: Wait for and disable HP-specific notification toggle in Windows Settings")
    toggle_image = screenshot_path + "windows_hp_notification_toggle_on.png"
    toggle_location = wait_for_image(toggle_image, timeout=15)
    pyautogui.click(toggle_location)
    pyautogui.press('space')  # This toggles it off
    time.sleep(2)

    logger.info("Step 4: Close Windows Settings (Alt+F4)")
    pyautogui.hotkey('alt', 'f4')
    time.sleep(2)

    logger.info("Step 5: Relaunch HPX and verify toggle is now OFF")
    launch_hpx_app()
    click_image(screenshot_path + "profile_icon.png")
    click_image(screenshot_path + "settings.png")
    assert wait_for_image(screenshot_path + "device_supply_toggle_off.png"), " Toggle did not change to OFF after disabling HP notifications"

    logger.info(" Toggle correctly updated to OFF based on Windows notification settings.")
    close_hpx_app()

#C53304249-ITG
@pytest.mark.device_navigation
def test_notification_section_and_device_status_visible():
    launch_hpx_app()
    wait_for_image(screenshot_path + "device_list.png")
    click_image(screenshot_path + "profile_icon.png")
    click_image(screenshot_path + "settings.png")
    assert wait_for_image(screenshot_path + "notification_section.png")
    assert wait_for_image(screenshot_path + "device&supply_status.png")
    close_hpx_app()
#C53304251-ITG
@pytest.mark.device_ui
def test_tc_004_device_and_supply_status_toggle_sequence():
    launch_hpx_app()
    click_image(screenshot_path + "profile_icon.png")
    click_image(screenshot_path + "settings.png")
    for _ in range(3):
        click_image(screenshot_path + "device_supply_toggle_on.png")
        click_image(screenshot_path + "device_supply_toggle_off.png")
    close_hpx_app()

#C53303684-only Available in HP laptops
@pytest.mark.profile_navigation
def test_navigate_to_support_page():
    launch_hpx_app()
    click_image(screenshot_path + "profile_icon.png")
    click_image(screenshot_path + "Support_btn.png")
    click_image(screenshot_path + "support_link_btn.png")
    assert wait_for_image(screenshot_path + "support_page_identifier.png")
    logger.info(" Support page loaded successfully.")
    close_hpx_app()

#C53304251-ITG
@pytest.mark.dependency_on_windows_notifications
def test_device_supply_status_toggle_depends_on_windows_notifications():
    logger.info("Launching Windows Notification Settings")
    subprocess.Popen("start ms-settings:notifications", shell=True)
    time.sleep(5)

    logger.info("Launching myHP and navigating to Notification Settings")
    launch_hpx_app()
    click_image(screenshot_path + "profile_icon.png")
    click_image(screenshot_path + "settings.png")

    toggle_status_img = screenshot_path + "device_supply_toggle_on.png"
    toggle_disabled_img = screenshot_path + "device_supply_toggle_off.png"

    if is_windows_notifications_enabled():
        assert wait_for_image(toggle_status_img), "Toggle should be enabled but is not."
        logger.info("Toggle is enabled as Windows notifications are enabled.")
    else:
        assert wait_for_image(toggle_disabled_img), "Toggle should be disabled but is not."
        logger.info("Toggle is disabled as Windows notifications are disabled.")

    close_hpx_app()
#C53303766-ITG
@pytest.mark.uri_launch
def test_launch_settings_page_via_uri():
    open_run_command_and_enter_uri()
    assert wait_for_image(settings_image), " Settings page not detected."
    logger.info(" Settings page opened via URI and verified.")
    close_hpx_app()

# ---------- CLI Runner ----------
if __name__ == "__main__":
    pytest.main(["-s", __file__])
