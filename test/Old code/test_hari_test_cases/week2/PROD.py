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

#C53303701-PROD
@pytest.mark.notification_flow
def test_tc_001_notifications_panel_opens():
    launch_hpx_app()
    time.sleep(10)

    logger.info("Step 1: Verify Device List screen is visible")
    assert wait_for_image(screenshot_path + "device_list_screen_prod.png"), "Device list screen not visible"
    time.sleep(2)

    logger.info("Step 2: Verify Global Header Navigation is visible")
    assert wait_for_image(screenshot_path + "global_header_nav.png"), "Global header navigation not found"
    time.sleep(2)

    logger.info("Step 3: Verify Bell Icon is visible under Global Header")
    assert wait_for_image(screenshot_path + "bell_icon.png"), "Bell icon not found under global header"
    time.sleep(2)

    logger.info("Step 4: Click Bell Icon to open notifications")
    assert wait_and_click(screenshot_path + "bell_icon.png"), "Failed to click Bell icon"
    time.sleep(5)

    logger.info("Step 5: Verify Notifications panel is visible")
    assert wait_for_image(screenshot_path + "notification_panel_prod.png"), "Notifications panel did not open"
    time.sleep(5)

    logger.info(" Test completed successfully")
    close_hpx_app()



#C53303925-PROD
@pytest.mark.account_creation
@pytest.mark.skip(reason="This test should only be executed when user logout every time to application")
def test_create_account_flow():
    launch_hpx_app()
    click_image(screenshot_path + "SignIn.png")
    time.sleep(15)
    click_image(screenshot_path + "create_account.png")
    enter_text(screenshot_path + "first_name_field.png", "Hari", tab_after=True)
    pyautogui.write("Prasad", interval=0.1)
    pyautogui.press('tab')
    pyautogui.write("hari@example.com", interval=0.1)
    pyautogui.press('tab')
    pyautogui.write("ValidPass123!", interval=0.1)
    click_image(screenshot_path + "terms_checkbox.png")
    pyautogui.scroll(1000)
    click_image(screenshot_path + "create_button.png")
    logger.info(" Account creation flow completed.")
    close_hpx_app()

#C53303926-PROD
@pytest.mark.account_creation
@pytest.mark.skip(reason="This test should only be executed when user logout every time to application")
def test_create_account_with_invalid_password():
    launch_hpx_app()
    click_image(screenshot_path + "SignIn.png")
    time.sleep(15)
    click_image(screenshot_path + "create_account.png")
    enter_text(screenshot_path + "first_name_field.png", "Test", tab_after=True)
    pyautogui.write("User", interval=0.1)
    pyautogui.press('tab')
    pyautogui.write("testuser@example.com", interval=0.1)
    pyautogui.press('tab')
    pyautogui.write("abc123", interval=0.1)
    click_image(screenshot_path + "terms_checkbox.png")
    pyautogui.scroll(300)
    click_image(screenshot_path + "create_button.png")
    assert wait_for_image(screenshot_path + "password_error_message.png", timeout=5)
    logger.info(" Password validation test completed.")
    close_hpx_app()

#C53303911-PROD
@pytest.mark.myhp_login_flow
@pytest.mark.skip(reason="This test should only be executed when user login first time to application")
def test_myhp_login_with_privacy_consent_repeat():
    # Renamed duplicate test function
    launch_hpx_app()
    scroll_privacy_screen(screenshot_path + "privacy_screen.png")
    click_image(screenshot_path + "Acceptall.png")
    time.sleep(5)
    click_image(screenshot_path + "signin_icon.png")
    time.sleep(10)
    enter_text(screenshot_path + "hpusername.png", "hari.vullithula@ascendion.com")
    click_image(screenshot_path + "hppassbutton.png")
    time.sleep(10)
    enter_text(screenshot_path + "hppassword.png", "Hari@7659")
    click_image(screenshot_path + "hpsignin.png")
    time.sleep(20)
    wait_for_image(screenshot_path + "Homescreen.png")
    wait_for_image(screenshot_path + "profile.png")
    logger.info(" myHP login flow repeat test completed successfully.")
    close_hpx_app()
#C53303927-PROD
@pytest.mark.mobile_input_validation
@pytest.mark.skip(reason="This test should only be executed when user logout every time to application")
def test_mobile_number_accepts_only_numbers():
    launch_hpx_app()
    click_image(screenshot_path + "SignIn.png")
    time.sleep(10)
    click_image(screenshot_path + "sign_in_with_mobile.png")
    clear_and_type(screenshot_path + "mobile_number_field.png", "abc123!@#")
    clear_and_type(screenshot_path + "mobile_number_field.png", "7659861017")
    logger.info(" Entered valid numeric input.")
    close_hpx_app()
#C53303909-PROD
@pytest.mark.myhp_login_flow
@pytest.mark.skip(reason="This test should only be executed when user login first time to application")
def test_myhp_login_with_privacy_consent():
    launch_hpx_app()
    scroll_privacy_screen(screenshot_path + "privacy_screen.png")
    click_image(screenshot_path + "Acceptall.png")
    time.sleep(5)
    click_image(screenshot_path + "signin_icon.png")
    time.sleep(10)
    enter_text(screenshot_path + "hpusername.png", "hari.vullithula@ascendion.com")
    click_image(screenshot_path + "hppassbutton.png")
    time.sleep(10)
    enter_text(screenshot_path + "hppassword.png", "Hari@7659")
    click_image(screenshot_path + "hpsignin.png")
    time.sleep(20)
    wait_for_image(screenshot_path + "Homescreen.png")
    wait_for_image(screenshot_path + "profile.png")
    logger.info(" myHP login flow test completed successfully.")
    close_hpx_app()
#C53303910-PROD
@pytest.mark.myhp_login_flow
@pytest.mark.skip(reason="This test should only be executed when user login first time to application")
def test_myhp_login_with_privacy_consent_repeat():
    # Renamed duplicate test function
    launch_hpx_app()
    scroll_privacy_screen(screenshot_path + "privacy_screen.png")
    click_image(screenshot_path + "Acceptall.png")
    time.sleep(5)
    click_image(screenshot_path + "signin_icon.png")
    time.sleep(10)
    enter_text(screenshot_path + "hpusername.png", "hari.vullithula@ascendion.com")
    click_image(screenshot_path + "hppassbutton.png")
    time.sleep(10)
    enter_text(screenshot_path + "hppassword.png", "Hari@7659")
    click_image(screenshot_path + "hpsignin.png")
    time.sleep(20)
    wait_for_image(screenshot_path + "Homescreen.png")
    wait_for_image(screenshot_path + "profile.png")
    logger.info(" myHP login flow repeat test completed successfully.")
    close_hpx_app()

# ---------- CLI Runner ----------
if __name__ == "__main__":
    pytest.main(["-s", __file__])
