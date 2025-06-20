import time
import pyautogui
import subprocess
import pytest

screenshot_path = "screenshot/"

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
    time.sleep(5)
    close_btn = pyautogui.locateCenterOnScreen(screenshot_path + "close_btn.png", confidence=0.7)
    time.sleep(5)
    pyautogui.moveTo(close_btn)
    pyautogui.click()
    time.sleep(2)


def validate_layout_exist(layout_list, context=""):
    """Checks if all images in the list are present on the screen."""
    for layout_name in layout_list:
        full_path = screenshot_path + layout_name
        location = wait_for_image(full_path)
        assert location is not None, f"{layout_name} not found {context}"

def click_close_usingXIcon():
   time.sleep(15)
   close_btn = wait_for_image(screenshot_path + "close_icon_X.png" ,confidence=0.8)
   assert close_btn is not None, "Close button not found on the screen"
   pyautogui.moveTo(close_btn)
   time.sleep(15)
   pyautogui.click(close_btn)
   time.sleep(2)
   pyautogui.click(close_btn)
   time.sleep(10)

@pytest.fixture(scope='module')
def launch_hpx_app():
    app_id = "AD2F1837.myHP_v10z8vjag6ke6!App"
    subprocess.Popen(f'explorer shell:AppsFolder\\{app_id}', shell=True)
    time.sleep(5)
    yield
    # optional teardown

def close_app_using_corner_x():
    """
    Closes the currently focused app by clicking the top-right corner 'X' button.
    Assumes the app window is maximized or 'X' is in top-right of the screen.
    """
    time.sleep(1)  # Optional wait to ensure UI is stable
    screen_width, _ = pyautogui.size()
    print(screen_width)
    x = screen_width - 10  # A few pixels from the right edge
    y = 10  # A few pixels from the top edge
    pyautogui.moveTo(x, y, duration=0.3)
    pyautogui.click()

# Test case 01
def test_tc_01_verify_app_only_consents_manage_choices_screen_accessibility(launch_hpx_app):
    "Verify App-only Consents->Manage Choices screen accessibility"
    time.sleep(5)
    pyautogui.scroll(-1000)
    pyautogui.press('pagedown')
    time.sleep(15)
    manage_choices_btn = wait_for_image(screenshot_path + "manage_choices_button.png" ,confidence=0.7)
    assert manage_choices_btn is not None, "Manage Choices button not found"
    time.sleep(2)
    pyautogui.moveTo(manage_choices_btn)
    pyautogui.click(manage_choices_btn)
    time.sleep(10)
    appscreen1 = wait_for_image(screenshot_path + "app_only_consents_screen1.png")
    assert appscreen1 is not None, "App-only Consents screen not displayed"
    time.sleep(5)
    pyautogui.scroll(-1000)
    time.sleep(2)
    appscreen2 = wait_for_image(screenshot_path + "app_only_consents_screen2.png")
    assert appscreen2 is not None, "App-only Consents screen not displayed"
    pyautogui.hotkey('alt', 'f4')
    click_close_usingXIcon()
      


# Test case 02
def test_tc_02_validate_app_only_consents_screen_content_for_row(launch_hpx_app):
    "Validate App-only Consents screen content for ROW"
    time.sleep(15)
    appscreen = wait_for_image(screenshot_path + "app_only_consents_screen.png")
    assert appscreen is not None, "App-only Consents screen not visible"
    time.sleep(3)
    data_privacy_title= wait_for_image(screenshot_path + "data_privacy_title.png")
    assert data_privacy_title is not None, "Data privacy title not found"
    time.sleep(5)
    we_value_your_privacy_heading = wait_for_image(screenshot_path + "we_value_your_privacy_heading.png")
    assert we_value_your_privacy_heading is not None, "we value your privacy not found"
    time.sleep(2)
    rowcontent = wait_for_image(screenshot_path + "row_content.png")
    assert rowcontent is not None, "ROW-specific content not found"
    pyautogui.hotkey('alt', 'f4')
    click_close_usingXIcon()

 # Test case 03
def test_tc_03_verify_buttons_layout_on_app_only_consents_manage_choices_page_for_row(launch_hpx_app):
    "Verify buttons layout on App-only Consents->Manage Choices page for ROW"
    time.sleep(15)
    pyautogui.scroll(-1000)
    time.sleep(2)
    pyautogui.press('pagedown')
    time.sleep(2)
    manage_choices_btn = wait_for_image(screenshot_path + "manage_choices_button.png" ,confidence=0.7)
    assert manage_choices_btn is not None, "Manage Choices button not found"
    time.sleep(2)
    pyautogui.moveTo(manage_choices_btn)
    pyautogui.click(manage_choices_btn)
    time.sleep(10)
    pyautogui.scroll(-1000)
    time.sleep(2)
    pyautogui.press('pagedown')
    layout_list = [
        "back_button.png",
        "continue_button.png",
    ]
    validate_layout_exist(layout_list, context="on Manage Choices ROW layout")
    pyautogui.hotkey('alt', 'f4')
    click_close_usingXIcon()
   




# Test case 9: Strictly Necessary Notice displays on the App-only Consents screen.
def test_tc_09_verify_strictly_necessary_notice(launch_hpx_app):

    consents_screen = wait_for_image(screenshot_path + "app_only_consents_screen.png" ,timeout=10, confidence=0.5)
    assert consents_screen is not None, "App-only Consents screen not displayed after launch."
    time.sleep(5)
    # Step 2: Validate that the strictly necessary notice is displayed.
    strictly_necessary_notice = wait_for_image(screenshot_path + "strictly_necessary_notice.png", timeout=10)
    assert strictly_necessary_notice is not None, "Strictly necessary notice not displayed on App-only Consents screen."
    pyautogui.hotkey('alt', 'f4')
    click_close_usingXIcon()



if __name__ == '__main__':
    pytest.main([__file__])