import time
import pyautogui
import subprocess
import pytest
import pygetwindow as gw
import logging

logger = logging.getLogger(__name__)

# Constants
screenshot_path = 'screenshot/'
username = 'Karthik.m@ascendion.com'
password = '262202@Km'


def wait_for_image(image, timeout=15, confidence=0.6):
    """
    Waits for an image to appear on screen within the   timeout.

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
    time.sleep(20)
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

def create_hp_account():
    logger.info("login to hp account")
    if not activate_chrome_window():
        return

    time.sleep(10)
    create_account = wait_for_image(screenshot_path + "create_account.png")
    assert create_account is not None, "create_account not found"
    pyautogui.click(create_account)
    time.sleep(10)
    # Allow the page to fully load

    # Step 1: First name textbox
    first_name_box = wait_for_image(screenshot_path + "first_name_textbox.png", confidence=0.8)
    assert first_name_box is not None, "First name textbox not found"
    pyautogui.click(first_name_box)
    pyautogui.write("Karc")
    time.sleep(2)

    # Step 2: Last name textbox
    last_name = wait_for_image(screenshot_path + "last_name.png", confidence=0.8)
    assert last_name is not None, "Last name textbox not found"
    pyautogui.click(last_name)
    time.sleep(1)
    last_name_box = wait_for_image(screenshot_path + "last_name_textbox.png", confidence=0.8)
    assert last_name_box is not None, "Last name textbox not found"
    pyautogui.click(last_name_box)
    pyautogui.write("Mark")
    time.sleep(2)

    # Step 3: Email address textbox
    email_ = wait_for_image(screenshot_path + "email.png", confidence=0.8)
    assert email_ is not None, "Last name textbox not found"
    pyautogui.click(email_)
    time.sleep(1)
    email_box = wait_for_image(screenshot_path + "email_textbox.png", confidence=0.8)
    assert email_box is not None, "Email address textbox not found"
    pyautogui.click(email_box)
    pyautogui.write(username)
    time.sleep(2)

    # Step 4: Password textbox
    password_ = wait_for_image(screenshot_path + "password.png", confidence=0.8)
    assert password_ is not None, "Last name textbox not found"
    pyautogui.click(password_)
    time.sleep(1)
    password_box = wait_for_image(screenshot_path + "password_textbox.png", confidence=0.8)
    assert password_box is not None, "Password textbox not found"
    pyautogui.click(password_box)
    pyautogui.write(password, interval=0.1)
    time.sleep(2)

    # Step 5: Optional checkbox - skip or enable based on your needs
    # checkbox = wait_for_image(screenshot_path + "checkbox_off.png", confidence=0.8)
    # if checkbox:
    #     pyautogui.click(checkbox)
    pyautogui.press('enter')  # Submit

    time.sleep(10)  # Wait for any redirect or confirmation


def login_hp_account():
    logger.info("login to hp account")
    if not activate_chrome_window():
        return
    time.sleep(10)  # Wait for page to fully load
    # user = wait_for_image(screenshot_path + "username_or_email_address.png")
    # assert user is not None, "Avatar icon not found on the device list screen"
    # pyautogui.click(user)
    # time.sleep(2)
    username_or_email_address_textbox = wait_for_image(screenshot_path + "username_or_email_address_textbox.png")
    assert username_or_email_address_textbox is not None, "username_or_email_address_textbox not found"
    pyautogui.click(username_or_email_address_textbox)
    pyautogui.write(username)
    pyautogui.press('tab', 2)  # Press tab twice to navigate to password field
    pyautogui.press('enter')
    time.sleep(5)
    passwword_text_box = wait_for_image(screenshot_path + "passwword_text_box.png")
    assert passwword_text_box is not None, "passwword_text_box not found"
    pyautogui.click(passwword_text_box)
    pyautogui.write(password, interval=0.1)  # Type password with a slight delay
    pyautogui.press('tab', 2)
    pyautogui.press('enter')  # Submit
    time.sleep(15)  # wait for sign in to complete


def logout_hp_account():
    logger.info("log out to hp account")
    initials = wait_for_image(screenshot_path + "profile_icon.png")
    pyautogui.click(initials)
    time.sleep(4)
    settings = wait_for_image(screenshot_path + "settings_option.png")
    pyautogui.click(settings)
    time.sleep(4)
    pyautogui.scroll(-500)
    time.sleep(1)
    sign_out_btn = wait_for_image(screenshot_path + "signout.png")
    assert sign_out_btn is not None, "Sign-out button not found"
    pyautogui.click(sign_out_btn)
    time.sleep(8)

# Test case C53303891
# @pytest.mark.usefixtures('launch_hpx_app')
# def test__c53303891_sign_in_and_sign_out_verify_user_can_create_account():
#     hpx_app_screen = wait_for_image(screenshot_path + "hpx_app.png", confidence=0.8)
#     assert hpx_app_screen is not None, "HPX app did not launch successfully"
#
#     # Step 2: Click on the "Sign in/Create account" button
#     sign_in_option = wait_for_image(screenshot_path + "Signin.png")
#     assert sign_in_option is not None, "Sign-in option not found in Bell Flyout"
#     pyautogui.click(sign_in_option)
#     activate_chrome_window()
#     create_hp_account()





# Test case C53303890
@pytest.mark.usefixtures('launch_hpx_app')
def test__c53303890_sign_in_and_sign_out_verify_redirect_to_external_browser():
    # Step 1: Launch HPX and verify the root view is displayed
    hpx_app_screen = wait_for_image(screenshot_path + "hpx_app.png", confidence=0.8)
    assert hpx_app_screen is not None, "HPX app did not launch successfully"
    time.sleep(8)
    avatar_icon = wait_for_image(screenshot_path + "avatar.png")
    assert avatar_icon is not None, "Avatar icon not found on Root view"
    pyautogui.click(avatar_icon)
    time.sleep(5)

    # Step 2: Click on the "Sign in/Create account" button
    sign_in_option = wait_for_image(screenshot_path + "GB_Signin.png")
    assert sign_in_option is not None, "Sign-in option not found in Bell Flyout"
    pyautogui.click(sign_in_option)
    activate_chrome_window()
    login_hp_account()
    logout_hp_account()

 # Test case C53303889
@pytest.mark.usefixtures('launch_hpx_app')
def test__c53303889_sign_in_and_sign_out_verify_button_click_functionality():
    # Step 1: Launch HPX and verify the root view is displayed
    hpx_app_screen = wait_for_image(screenshot_path + "hpx_app.png", confidence=0.8)
    assert hpx_app_screen is not None, "HPX app did not launch successfully"

    # Step 2: Locate and click on the Avatar icon
    avatar_icon = wait_for_image(screenshot_path + 'avatar.png')
    assert avatar_icon is not None, "Avatar icon missing on the root view."
    pyautogui.click(avatar_icon)
    time.sleep(2)

    # Step 3: Locate and click on the Sign-in/Create Account button
    signin_createaccount = wait_for_image(screenshot_path + 'GB_Signin.png')
    assert signin_createaccount is not None, "Sign-in/Create Account button not available."
    pyautogui.click(signin_createaccount)
    time.sleep(2)
    activate_chrome_window()
    login_hp_account()
    logout_hp_account()


# Test case C53303888
@pytest.mark.usefixtures('launch_hpx_app')
def test__c53303888_sign_in_and_sign_out_verify_account_option_visibility():
    # Step 1: Launch HPX and verify the root view is visible
    hpx_app_screen = wait_for_image(screenshot_path + "hpx_app.png", confidence=0.8)
    assert hpx_app_screen is not None, "HPX app did not launch successfully"

    # Step 2: Locate and click on the Avatar icon
    avatar_icon = wait_for_image(screenshot_path + 'avatar.png')
    assert avatar_icon is not None, "Avatar icon missing on the root view."
    pyautogui.click(avatar_icon)
    time.sleep(2)

    # Step 3: Locate and click on the Sign-in/Create Account button
    signin_createaccount = wait_for_image(screenshot_path + 'GB_Signin.png')
    assert signin_createaccount is not None, "Sign-in/Create Account button not available."
    pyautogui.click(signin_createaccount)
    time.sleep(2)
    activate_chrome_window()
    login_hp_account()


# Test case C53303886
@pytest.mark.usefixtures('launch_hpx_app')
def test__c53303886_sign_in_verify_close_button_visibility_and_click():
    # Step 1: Launch HPX and verify the root view is displayed
    hpx_app_screen = wait_for_image(screenshot_path + "hpx_app.png", confidence=0.8)
    assert hpx_app_screen is not None, "HPX app did not launch successfully"

    # Step 2: Locate and click on the Avatar icon on the Root view
    profile_icon = wait_for_image(screenshot_path + 'profile_icon.png', timeout=10)
    assert profile_icon is not None, "Avatar icon not visible on root view."
    pyautogui.click(profile_icon)
    time.sleep(2)
    click_on_close_button()

# Test case C53303887
@pytest.mark.usefixtures('launch_hpx_app')
def test__c53303887_sign_in_verify_close_button_redirects_to_root():
    # Step 1: Launch HPX and confirm the root view is displayed
    hpx_app_screen = wait_for_image(screenshot_path + "hpx_app.png", confidence=0.8)
    assert hpx_app_screen is not None, "HPX app did not launch successfully"

    # Step 2: Locate and click on the Avatar icon
    profile_icon = wait_for_image(screenshot_path + 'profile_icon.png', timeout=10)
    assert profile_icon is not None, "Avatar icon not found on launch."
    pyautogui.click(profile_icon)
    time.sleep(2)
    user_icon = wait_for_image(screenshot_path + 'user_icon.png')
    assert user_icon is not None, "Avatar icon not found on launch."
    time.sleep(2)
    click_on_close_button()

# Test case C53303885
@pytest.mark.usefixtures('launch_hpx_app')
def test__c53303885_sign_in_and_sign_out_verify_navigation_panel_opens():
    # Step 1: Launch HPX and verify display of the root view
    hpx_app_screen = wait_for_image(screenshot_path + "hpx_app.png", confidence=0.8)
    assert hpx_app_screen is not None, "HPX app did not launch successfully"

    # Step 2: Locate and click on the Avatar icon
    profile_icon = wait_for_image(screenshot_path + 'profile_icon.png', timeout=10)
    assert profile_icon is not None, "Avatar icon not present on root view."
    pyautogui.click(profile_icon)
    time.sleep(2)
    click_on_close_button()


# Test case C53303884
@pytest.mark.usefixtures('launch_hpx_app')
def test__c53303884_sign_in_and_sign_out_verify_avatar_icon_clickable():
    # Step 1: Launch HPX and check that the root view is visible
    hpx_app_screen = wait_for_image(screenshot_path + "hpx_app.png", confidence=0.8)
    assert hpx_app_screen is not None, "HPX app did not launch successfully"

    # Step 2: Locate the Avatar icon and click it
    profile_icon = wait_for_image(screenshot_path + 'profile_icon.png', timeout=10)
    assert profile_icon is not None, "Avatar icon not detected on root view."
    pyautogui.click(profile_icon)
    print("avatar icon clicked")
    time.sleep(2)
    click_on_close_button()


# Test case C53303882
@pytest.mark.usefixtures('launch_hpx_app')
def test__c53303882_sign_in_and_sign_out_verify_avatar_icon_visibility():
    # Step 1: Launch HPX and verify the root view is displayed
    hpx_app_screen = wait_for_image(screenshot_path + "hpx_app.png", confidence=0.8)
    assert hpx_app_screen is not None, "HPX app did not launch successfully"
    time.sleep(1)
    logout_hp_account()
    time.sleep(2)

# #Test case C53303963: Verify App Close
@pytest.mark.usefixtures('launch_hpx_app')
def test_c53303963_verify_app_close_by_clicking_x(launch_hpx_app):
    # Step 1: Confirm HPX app launched successfully
    hpx_app_screen = wait_for_image(screenshot_path + 'hpx_app.png', timeout=15)
    assert hpx_app_screen is not None, 'HPX application did not launch.'

    # Step 2: Locate and click the "X" (close) button on the HPX window
    close_button = wait_for_image(screenshot_path + 'close.png', confidence=0.8, timeout=10)
    assert close_button is not None, '"X" (close) button not found on HPX app window.'
    pyautogui.click(close_button)
    time.sleep(5)