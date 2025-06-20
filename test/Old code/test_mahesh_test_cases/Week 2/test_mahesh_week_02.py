import time
import pyautogui
import subprocess
import pytest
import pygetwindow as gw
import logging

logger = logging.getLogger(__name__)

# Constants
screenshot_path = "screenshot/mahesh_dark_mode/"
username = 'maheshkumar.s@ascendion.com'
password = 'Mahesh@29061996'


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
    time.sleep(35)
    yield True

    # --- Teardown Logic using subprocess ---
    print("Closing HPX App...")
    try:
        # Replace with the actual process name of your app
        subprocess.run(["taskkill", "/f", "/im", "HP.myHP.exe"], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except subprocess.CalledProcessError:
        print("Warning: HPX App might already be closed or not found.")

def login_hp_account():
    logger.info("login to hp account")
    if not activate_chrome_window():
        return
    time.sleep(10)  # Wait for page to fully load
    username_or_email_address_textbox = wait_for_image("username_txtbox.png")
    assert username_or_email_address_textbox is not None, "username_or_email_address_textbox not found"
    pyautogui.click(username_or_email_address_textbox)
    pyautogui.write(username)
    pyautogui.press('tab',2) # Press tab twice to navigate to password field
    pyautogui.press('enter')
    time.sleep(5)
    passwword_text_box = wait_for_image("password_txtbox.png")
    assert passwword_text_box is not None, "passwword_text_box not found"
    pyautogui.click(passwword_text_box)
    pyautogui.write(password,interval=0.1)  # Type password with a slight delay
    pyautogui.press('tab',2)
    pyautogui.press('enter')   # Submit
    time.sleep(10) #wait for sign in to completed


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

# Test case C53542821
# Verify that "Continue as Guest" present on Welcome screen navigates to device list page
#def test_tc_C53542821_(launch_hpx_app):



# Verify that "Sign In" and "Continue as Guest " button appear on Welcome Screen
def test_tc_C53533727_(launch_hpx_app):

    sign_in_option = wait_for_image(screenshot_path + "signin_btn.png", timeout=10, confidence=0.8)
    assert sign_in_option is not None, "Sign-in option not found in Bell Flyout"

# Test case C53542819
# Verify that Sign In button present on Welcome Screen navigates to external browser
def test_tc_C53542819_(launch_hpx_app):

    sign_in_option = wait_for_image(screenshot_path + "signin_btn.png", timeout=10, confidence=0.8)
    assert sign_in_option is not None, "Sign-in option not found in Bell Flyout"
    pyautogui.click(sign_in_option)
    activate_chrome_window()
    login_hp_account()

# Test case C53542592
# Verify that Welcome Screen is not displayed when we close the application on Welcome Screen and relaunch the application
def test_tc_C53542592_(launch_hpx_app):

    close_button_location = wait_for_image(screenshot_path + "x_btn.png", timeout=10, confidence=0.8)
    assert close_button_location is not None, "Close (X) button not found."
    pyautogui.moveTo(close_button_location)
    pyautogui.click()
    time.sleep(5)  #
    relaunch_hpx_app()

# Test case C53681220
# Verify the feedback is present and accessible through the Panel Navigation in the HPX app
def test_tc_C53681220_(launch_hpx_app):

    device_list = wait_for_image(screenshot_path + "device_details_btn.png", timeout=10, confidence=0.8)
    assert device_list is not None, "Device List option not found in Home Flyout"
    pyautogui.click(device_list)
    time.sleep(1)

    profile_icon = wait_for_image(screenshot_path + "profile_icon.png", timeout=10, confidence=0.8)
    assert profile_icon is not None, "profile icon option not found in home Flyout"
    pyautogui.click(profile_icon)
    time.sleep(1)

    feedback_button = wait_for_image(screenshot_path + "feedback_btn.png", timeout=10, confidence=0.8)
    assert feedback_button is not None, "Feedback Button Not found in Home Flyout"
    pyautogui.click(feedback_button)
