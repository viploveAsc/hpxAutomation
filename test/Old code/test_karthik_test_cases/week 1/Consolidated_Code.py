import time
import pyautogui
import subprocess
import pytest
import pygetwindow as gw
import logging

logger = logging.getLogger(__name__)

# Constants
screenshot_path = 'screenshot/'
username = 'karthik.m@ascendion.com'
password = '262202@Km'


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
    sign_out_btn = wait_for_image(screenshot_path + "signout.png")
    assert sign_out_btn is not None, "Sign-out button not found"
    pyautogui.click(sign_out_btn)
    time.sleep(8)


def test_tc_16_bell_notifications_login_using_sign_in_option_in_bell_flyout(launch_hpx_app):
    # Step 1: Launch HPX app - verifying that the app is launched successfully
    hpx_app_screen = wait_for_image(screenshot_path + "hpx_app.png", confidence=0.8)
    assert hpx_app_screen is not None, "HPX app did not launch successfully"

    # Step 2: Click on the "Sign in/Create account" button
    sign_in_option = wait_for_image(screenshot_path + "Signin.png")
    assert sign_in_option is not None, "Sign-in option not found in Bell Flyout"
    pyautogui.click(sign_in_option)
    activate_chrome_window()
    login_hp_account()




# Test case C53303765 - [HPX][Settings] Verify the Settings side panel when the user is signed_in
def test_c53303765_hpx_settings_verify_settings_side_panel_when_signed_in(launch_hpx_app):
    # Step 1: Launch HPX app - verifying that the app is launched successfully
    hpx_app_screen = wait_for_image(screenshot_path + "hpx_app.png", confidence=0.8)
    assert hpx_app_screen is not None, "HPX app did not launch successfully"

    # Step 2: Verify that the Root View/Device list is displayed
    device_list_screen = wait_for_image(screenshot_path + "device_list.png")
    assert device_list_screen is not None, "Device list not displayed on Root view"

    # Step 3: Observe the Avatar icon on the Root View/Device list
    profile_icon = wait_for_image(screenshot_path + "profile_icon.png")
    assert profile_icon is not None, "Avatar icon not found on the device list screen"
    pyautogui.click(profile_icon)
    time.sleep(2)

    # Step 5: Click on the Settings button
    settings_button = wait_for_image(screenshot_path + "settings_option.png")
    assert settings_button is not None, "Settings button not found on the screen"
    pyautogui.click(settings_button)
    time.sleep(2)

    # Step 6: Scroll to the bottom of the Settings screen
    pyautogui.scroll(-500)
    time.sleep(2)
    pyautogui.scroll(+1000)
    time.sleep(2)
    menu_button = wait_for_image(screenshot_path + "menu_button.png")
    pyautogui.click(menu_button)
    click_on_close_button()



# Test case C53303763 - [HPX][Settings] Verify that clicking the Settings button opens the Settings side panel correctly
def test_c53303763_hpx_settings_verify_clicking_settings_opens_side_panel(launch_hpx_app):
    # Step 1: Launch myHP app - assuming similar behavior as HPX app
    device_list_screen = wait_for_image(screenshot_path + "device_list.png", confidence=0.8)
    assert device_list_screen is not None, "myHP app did not launch"
    pyautogui.click(device_list_screen)
    time.sleep(5)

    # # Step 2: Verify that the device list/device details page is displayed
    # device_details = wait_for_image(screenshot_path + "device_details_pg.png")
    # assert device_details is not None, "Device list/details page not displayed"
    # time.sleep(2)

    # Step 3: Click on the Profile button at the right of the screen
    profile_button = wait_for_image(screenshot_path + "profile_icon.png")
    assert profile_button is not None, "Profile button not found on the screen"
    pyautogui.click(profile_button)
    time.sleep(2)

    # Step 4: Click on the Settings option
    settings_option = wait_for_image(screenshot_path + "settings_option.png")
    assert settings_option is not None, "Settings option not found on the screen"
    pyautogui.click(settings_option)
    time.sleep(2)
    menu_button = wait_for_image(screenshot_path + "menu_button.png")
    pyautogui.click(menu_button)
    click_on_close_button()
    time.sleep(2)
    device_button = wait_for_image(screenshot_path + "device_btn.png")
    pyautogui.click(device_button)
    time.sleep(2)

# Test case C53303761 - [HPX][Settings] Verify the functionality of the menu button present on the Settings side panel
def test_c53303761_hpx_settings_verify_settings_menu_button_functionality(launch_hpx_app):
    # hpx_app_screen = wait_for_image(screenshot_path + "hpx_app.png", confidence=0.8)
    # assert hpx_app_screen is not None, "HPX app did not launch successfully"
    # time.sleep(2)

    # # Step 2: Verify that the Root View/Device list is displayed
    # device_list_screen = wait_for_image(screenshot_path + "device_list.png")
    # assert device_list_screen is not None, "Device list not displayed on Root view"

    # Step 3: Observe the Avatar icon on the Root View/Device list
    profile_icon = wait_for_image(screenshot_path + "profile_icon.png")
    assert profile_icon is not None, "Avatar icon not found on the device list screen"
    pyautogui.click(profile_icon)
    time.sleep(2)



    # Step 4: Click on the Menu button present on the Settings slide-out panel
    settings_option = wait_for_image(screenshot_path + "settings_option.png")
    assert settings_option is not None, "Settings option not found on the screen"
    pyautogui.click(settings_option)
    time.sleep(2)
    menu_button = wait_for_image(screenshot_path + "menu_button.png")
    pyautogui.click(menu_button)
    time.sleep(2)
    click_on_close_button()
    time.sleep(2)


# Test case C53303760 - [HPX][Settings] Verify the menu button is present on the Settings side panel
def test_c53303760_hpx_settings_verify_menu_button_presence_on_settings_panel(launch_hpx_app):
    # Step 1: Launch myHP app
    hpx_app_screen = wait_for_image(screenshot_path + "hpx_app.png", confidence=0.8)
    assert hpx_app_screen is not None, "HPX app did not launch successfully"

    # Step 2: Verify that the device list/details page is displayed
    # device_details = wait_for_image(screenshot_path + "device_list.png")
    # assert device_details is not None, "Device list/details page not displayed"

    # Step 3: Click on the Profile button
    profile_button = wait_for_image(screenshot_path + "profile_icon.png")  # Corrected image name
    assert profile_button is not None, "Profile button not found"
    pyautogui.click(profile_button)
    time.sleep(2)

    # Step 4: Click on the Settings option
    settings_option = wait_for_image(screenshot_path + "settings_option.png")
    assert settings_option is not None, "Settings option not found"
    pyautogui.click(settings_option)
    time.sleep(2)

    # Step 5: Verify the Menu button is visible on the Settings side panel
    menu_button = wait_for_image(screenshot_path + "menu_button.png")
    assert menu_button is not None, "Menu button not visible on settings side panel"
    pyautogui.click(menu_button)
    time.sleep(2)
    click_on_close_button()
    time.sleep(2)


# Test case C53303759 - [HPX][Settings] Verify the Global side panel is opened upon clicking on the Avatar button
def test_c53303759_hpx_settings_verify_global_side_panel_opens_on_avatar_click(launch_hpx_app):
    # Detailed steps not provided. Please implement when available.
    pass


# Test case C53303758 - [HPX][Settings] Verify the user is able to click on the Avatar that is visible on the Global Nav Panel
def test_c53303758_hpx_settings_verify_avatar_clickable_on_global_nav_panel(launch_hpx_app):
    # Detailed steps not provided. Please implement when available.
    pass


# Test case C53303757 - [HPX][Settings] Verify the Avatar is visible on the Global Nav Panel
def test_c53303757_hpx_settings_verify_avatar_visibility_on_global_nav_panel(launch_hpx_app):
    # Detailed steps not provided. Please implement when available.
    pass


# Test case C53303756 - [HPX][Settings] Verify the Navigation side Panel or the Global sidebar is accessible from the Device list page/Root view
def test_c53303756_hpx_settings_verify_navigation_side_panel_accessible_from_device_list(launch_hpx_app):
    # Step 1: Launch HPX app
    hpx_app_screen = wait_for_image(screenshot_path + "hpx_app.png", confidence=0.8)
    assert hpx_app_screen is not None, "HPX app did not launch successfully"

    # Step 2: Verify that the Root view/Device list screen is displayed
    device_list = wait_for_image(screenshot_path + "device_list.png")
    assert device_list is not None, "Device list screen not displayed"


    # Step 3: Click on the Avatar icon on the right side of the screen
    avatar_icon = wait_for_image(screenshot_path + "profile_icon.png")
    assert avatar_icon is not None, "Avatar icon not found on device list screen"
    pyautogui.click(avatar_icon)
    click_on_close_button()
    time.sleep(2)

# Test case C53533732: Global Side bar UI visibility with signed in State
def test_c53533732_global_sidebar_ui_with_signed_in_state(launch_hpx_app):
    # Step 1: Launch HPX (Assumed by fixture)
    hpx_app_screen = wait_for_image(screenshot_path + "hpx_app.png", confidence=0.8)
    assert hpx_app_screen is not None, "HPX app did not launch successfully"

    # Step 2: Stay signed in and land on home page, then click on Profile Icon
    profile_button = wait_for_image(screenshot_path + "profile_icon.png")  # Corrected image name
    assert profile_button is not None, "Profile button not found"
    pyautogui.click(profile_button)
    time.sleep(2)

    # Step 3: Validate Global sidebar UI is visible
    global_sidebar = wait_for_image(screenshot_path + 'global_side_panel.png', timeout=10)
    assert global_sidebar is not None, 'Global side bar UI did not display as expected.'
    time.sleep(2)
    click_on_close_button()


# Test case C53303686: Navigate to Settings page
@pytest.mark.usefixtures('launch_hpx_app')
def test_c53303686_navigate_to_settings_page(launch_hpx_app):
    # Step 1: Launch myHP application (Assumed by fixture)
    hpx_window = wait_for_image(screenshot_path + 'hpx_app.png', timeout=15)
    assert hpx_window is not None, 'myHP application did not launch.'

    # Step 2: Click on the Profile Icon/Avatar
    profile_icon = wait_for_image(screenshot_path + 'profile_icon.png', timeout=10)
    assert profile_icon is not None, 'Profile icon not found.'
    pyautogui.click(profile_icon)
    time.sleep(2)

    # Step 3: Click on the Settings button
    settings_button = wait_for_image(screenshot_path + 'settings_option.png', timeout=10)
    assert settings_button is not None, 'Settings button not found.'
    pyautogui.click(settings_button)
    time.sleep(3)
    menu_button = wait_for_image(screenshot_path + 'menu_button.png', timeout=10)
    pyautogui.click(menu_button)
    time.sleep(2)
    click_on_close_button()




# Test case C53303687 - Navigate to Feedback page
@pytest.mark.usefixtures('launch_hpx_app')
def test_c53303687_navigate_to_feedback_page(launch_hpx_app):
    # Step 1: Click on the profile icon/Avatar
    profile_icon = wait_for_image(screenshot_path + 'profile_icon.png')
    assert profile_icon is not None, "Profile icon not found on screen"
    pyautogui.click(profile_icon)
    time.sleep(1)

    # Step 2: Click on the Feedback button
    feedback_button = wait_for_image(screenshot_path + 'feedback_button.png')
    assert feedback_button is not None, "Feedback button not found on screen"
    pyautogui.click(feedback_button)
    time.sleep(2)
    menu_button = wait_for_image(screenshot_path + "menu_button.png")
    pyautogui.click(menu_button)
    click_on_close_button()



# Test case C53303689 - App Window resize (Global Sidebar)
@pytest.mark.usefixtures('launch_hpx_app')
def test_c53303689_app_window_resize(launch_hpx_app):
        # Step 1: Verify HPX Application launch
        app_launch = wait_for_image(screenshot_path + "hpx_app.png")
        assert app_launch is not None, "HPX-Application did not launch as expected."

        # Step 2: Resize app using minimize and maximize button
        minimize_btn = wait_for_image(screenshot_path + "maximize.png")
        assert minimize_btn is not None, "Minimize button not found."
        pyautogui.click(minimize_btn)
        time.sleep(2)

@pytest.mark.usefixtures('launch_hpx_app')
def test_c53304013_app_window_resize(launch_hpx_app):
        maximize_btn = wait_for_image(screenshot_path + "minimize.png")
        assert maximize_btn is not None, "Maximize button not found."
        pyautogui.click(maximize_btn)
        time.sleep(2)


# Test case C53304001 - Validating response of Bell button on clicking
@pytest.mark.usefixtures('launch_hpx_app')
def test_c53304001_validating_response_of_bell_button(launch_hpx_app):
    # Step 1: Launch myHP application and click on Bell Notification button

    bell_notification = wait_for_image(screenshot_path + 'img.png')
    assert bell_notification is not None, "Bell notification button not found"
    pyautogui.click(bell_notification)
    time.sleep(2)
    click_on_close_button()






# Test case C53304010 - Hover State - Notification
@pytest.mark.usefixtures('launch_hpx_app')
def test_c53304010_hover_state_notification(launch_hpx_app):
    # Step 1: Launch myHP application and hover on the Bell icon on Top Bar
    bell_icon = wait_for_image(screenshot_path + 'img.png')
    assert bell_icon is not None, "Bell icon not found for hover action"
    pyautogui.moveTo(bell_icon)
    time.sleep(2)

    # Step 2: Click bell icon button
    pyautogui.click(bell_icon)
    time.sleep(2)
    click_on_close_button()

#Test_case C53303688 - Close button
@pytest.mark.usefixtures('launch_hpx_app')
def test_c53303688_close_button(launch_hpx_app):
    # Step 1: Launch hpx rebrand application and navigate to global sidebar
    profile_icon = wait_for_image(screenshot_path + 'profile_icon.png')
    assert profile_icon is not None, "Profile icon not found on screen"
    pyautogui.click(profile_icon)
    time.sleep(1)
    global_sidebar = wait_for_image(screenshot_path + 'global_side_panel.png')
    assert global_sidebar is not None, "Global sidebar is not visible"
    time.sleep(1)

    # Step 2: Click on the close button using the reusable function
    click_on_close_button()

# Test case C53304000 - Validation of TopNavBar in Signed In state
@pytest.mark.usefixtures('launch_hpx_app')
def test_c53304000_validation_of_top_nav_signed_in_state(launch_hpx_app):
    # Step 1: Launch myHP application and sign in to the application
    sign_in = wait_for_image(screenshot_path + 'profile_icon.png')
    assert sign_in is not None, "Sign in option not found on screen"
    time.sleep(3)
      # Step 2: Observe the Top Navigation Bar


#
# #Test case C53303963: Verify App Close
# @pytest.mark.usefixtures('launch_hpx_app')
# def test_c53303963_verify_app_close_by_clicking_x(launch_hpx_app):
#     # Step 1: Confirm HPX app launched successfully
#     hpx_app_screen = wait_for_image(screenshot_path + 'hpx_app.png', timeout=15)
#     assert hpx_app_screen is not None, 'HPX application did not launch.'
#
#     # Step 2: Locate and click the "X" (close) button on the HPX window
#     close_button = wait_for_image(screenshot_path + 'close.png', confidence=0.8, timeout=10)
#     assert close_button is not None, '"X" (close) button not found on HPX app window.'
#     pyautogui.click(close_button)
#     time.sleep(5)
#
#
# # Test case C53303966: launching HPX App through CMD
# @pytest.mark.usefixtures('launch_hpx_app')
# def test_c53303966_launching_hpx_app_through_cmd(launch_hpx_app):
#     # Step 1: Wait for CMD window to open
#     print("Waiting for CMD window to open...")
#     cmd_window = wait_for_image(screenshot_path + 'img_1.png', timeout=15)
#     assert cmd_window is not None, "CMD window not found! Make sure CMD is open and visible."
#
#     # Click on CMD window to focus it
#     pyautogui.click(cmd_window)
#     time.sleep(1)  # small pause to ensure focus
#
#     # Step 2: Type the command to launch HPX app and press Enter
#     pyautogui.write('myHP', interval=0.1)  # type slowly for reliability
#     pyautogui.press('enter')
#     time.sleep(5)  # wait for the app to launch
#
#     # Step 3: Verify HPX app window is visible on screen
#     hpx_window = wait_for_image(screenshot_path + 'hpx_app.png', timeout=20)
#     assert hpx_window is not None, 'HPX app did not launch after typing the command.'



# Test case C53304002 - Validating response of Avatar icon on clicking
@pytest.mark.usefixtures('launch_hpx_app')
def test_c53304002_validating_response_of_avatar_icon(launch_hpx_app):
        # Step 1: Launch myHP application (Assumed by fixture)
        hpx_window = wait_for_image(screenshot_path + 'hpx_app.png', timeout=15)
        assert hpx_window is not None, 'myHP application did not launch.'

        # Step 2: Click on the Profile Icon/Avatar
        profile_icon = wait_for_image(screenshot_path + 'profile_icon.png', timeout=10)
        assert profile_icon is not None, 'Profile icon not found.'
        pyautogui.click(profile_icon)
        time.sleep(2)

        # Step 3: Click on the Settings button
        settings_button = wait_for_image(screenshot_path + 'settings_option.png', timeout=10)
        assert settings_button is not None, 'Settings button not found.'
        pyautogui.click(settings_button)
        time.sleep(3)
        logout_button = wait_for_image(screenshot_path + 'signed_out.png', timeout=10)
        assert logout_button is not None, 'Signout button not found.'
        pyautogui.click(logout_button)
        time.sleep(25)

#Test case C53303683: User is not signed in
@pytest.mark.usefixtures('launch_hpx_app')
def test_c53303683_user_not_signed_in_global_sidebar(launch_hpx_app):
    # Step 1: Launch myHP application without signing in
    hpx_window = wait_for_image(screenshot_path + 'hpx_app.png', timeout=15)
    assert hpx_window is not None, 'myHP application did not launch.'

    # Step 2: Click on the Profile Icon/Avatar
    profile_icon = wait_for_image(screenshot_path + 'avatar.png', timeout=10)
    assert profile_icon is not None, 'Profile icon not found for unsigned user.'
    pyautogui.click(profile_icon)
    time.sleep(2)
    click_on_close_button()
    time.sleep(2)

 # Test case C53303762 - [HPX][Settings] Verify the Settings option is visible and on the Global side panel and it can be clicked
def test_c53303762_hpx_settings_verify_settings_option_visible_and_clickable(launch_hpx_app):
    # Step 1: Launch HPX app - verification already done by fixture
    hpx_app = wait_for_image(screenshot_path + "hpx_app.png")
    assert hpx_app is not None, "HPX app did not launch successfully"

    # Step 2: On the Root view/Device list, click on the Avatar icon to check UI state (signed in)
    avatar_icon = wait_for_image(screenshot_path + "avatar.png")
    assert avatar_icon is not None, "Avatar icon not found on Root view"
    pyautogui.click(avatar_icon)
    time.sleep(5)


    # Step 4: Click on the Settings option
    settings_button = wait_for_image(screenshot_path + "settings_option.png")
    assert settings_button is not None, "Settings button not found on the screen"
    pyautogui.click(settings_button)
    time.sleep(2)
    menu_button = wait_for_image(screenshot_path + "menu_button.png")
    assert menu_button is not None, "Menu button not visible on settings side panel"
    pyautogui.click(menu_button)
    time.sleep(2)
    click_on_close_button()
    time.sleep(2)


# Test case C53303960: Verify Top App Bar Icons
def test_c53303960_verify_top_app_bar_icons(launch_hpx_app):
    # Step 1: Launch HPX (Assume already launched by fixture)
    hpx_window = wait_for_image(screenshot_path + 'hpx_app.png', confidence=0.8)
    assert hpx_window is not None, 'HPX application did not launch.'

    # Step 2: Verify Top App Bar icons are visible
    # add_device_icon = wait_for_image(screenshot_path + 'add_device.png', timeout=10)
    # assert add_device_icon is not None, 'Add Device icon not visible on Top App Bar.'

    bell_icon = wait_for_image(screenshot_path + 'img.png', timeout=10)
    assert bell_icon is not None, 'Bell icon not visible on Top App Bar.'

    avatar_icon = wait_for_image(screenshot_path + 'avatar.png', timeout=10)
    assert avatar_icon is not None, 'Avatar icon not visible on Top App Bar.'
    time.sleep(2)


    sign_in_icon = wait_for_image(screenshot_path + 'Signin.png', timeout=10)
    assert sign_in_icon is not None, 'Sign In button not visible on Top App Bar.'
    time.sleep(2)


# Test case C53304011 - Hover State - Profile and Settings
@pytest.mark.usefixtures('launch_hpx_app')
def test_c53304011_hover_state_profile_and_settings(launch_hpx_app):
    # Step 1: Launch myHP application and hover on the Profile icon on Top Bar
    profile_icon = wait_for_image(screenshot_path + 'avatar.png')
    assert profile_icon is not None, "Profile icon not found for hover action"
    pyautogui.moveTo(profile_icon)
    time.sleep(2)
    pyautogui.click(profile_icon)
    time.sleep(2)
    click_on_close_button()

    # Step 2: Click on the Profile and settings button
    # profile_settings = wait_for_image(screenshot_path + 'ProfileSettings.png')
    # assert profile_settings is not None, "Profile and settings button not visible when hovered"
    # pyautogui.click(profile_settings)
    # time.sleep(2)
    # click_on_close_button()


# Test case C53303964: launching HPX App close Al4+F4
@pytest.mark.usefixtures('launch_hpx_app')
def test_c53303964_verify_app_close_alt_f4():
    # Step 1: Confirm HPX app launched successfully
    hpx_app_screen = wait_for_image(screenshot_path + "hpx_app.png", confidence=0.8)
    assert hpx_app_screen is not None, "HPX app did not launch successfully"

    # Step 2: Send Alt+F4 to close the HPX application
    pyautogui.hotkey('alt', 'f4')
    time.sleep(3)


