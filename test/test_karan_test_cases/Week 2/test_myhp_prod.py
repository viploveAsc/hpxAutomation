import time
import pyautogui
import subprocess
import pytest
import pygetwindow as gw

screenshot_path = "screenshot/viplove_dark_mode/"
# Constants
username = 'viplove.bisen@gmail.com'
password = 'Vippy@1234'

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
        
def click_on_close_button():
    time.sleep(2)
    close_btn = pyautogui.locateCenterOnScreen(screenshot_path + "close_btn.png", confidence=0.7)
    pyautogui.moveTo(close_btn)
    pyautogui.click()
    time.sleep(2)

@pytest.fixture(scope='module')
def launch_hpx_app():
    app_id = "AD2F1837.myHP_v10z8vjag6ke6!App"
    subprocess.Popen(f'explorer shell:AppsFolder\\{app_id}', shell=True)
    time.sleep(3)
    yield
    # optional teardown
def activate_chrome_window():
    # Wait for Chrome to open and detect the correct window
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
    
if __name__ == '__main__':
    pytest.main([__file__])