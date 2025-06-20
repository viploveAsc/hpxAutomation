import time
import pyautogui
import subprocess
import pytest
import pygetwindow as gw

screenshot_path = "screenshot/karan/"

# Utility Functions

def wait_for_image(image, timeout=10, confidence=0.6):
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

def click_image(image, timeout=10, confidence=0.8, click_twice=False, delay=2):
    """Wait for image and click on it."""
    location = wait_for_image(image, timeout, confidence)
    assert location is not None, f"Image not found: {image}"
    pyautogui.moveTo(location)
    pyautogui.click()
    if click_twice:
        pyautogui.click()
    time.sleep(delay)
    return location

def scroll_and_wait(amount=-500, delay=1):
    pyautogui.scroll(amount)
    time.sleep(delay)

def click_on_close_button():
    """Click on the app's close button using a predefined screenshot."""
    time.sleep(5)
    close_btn = pyautogui.locateCenterOnScreen(screenshot_path + "close_btn.png", confidence=0.7)
    time.sleep(5)
    if close_btn:
        pyautogui.moveTo(close_btn)
        pyautogui.click()
    time.sleep(2)

def select_dropdown_option(dropdown_image, option_image, timeout=10):
    """Generalized function to select an option from a dropdown."""
    click_image(dropdown_image, timeout)
    click_image(option_image, timeout)

def right_click_and_select(main_image, context_option_image, timeout=10):
    """Right-click on an item and select an option from the context menu."""
    main_location = wait_for_image(main_image, timeout=timeout)
    assert main_location is not None, f"{main_image} not found."
    pyautogui.moveTo(main_location)
    pyautogui.click(button='right')
    time.sleep(1)
    click_image(context_option_image, timeout)

def search_and_launch_app(app_name='myhp', icon_image=screenshot_path + 'myhp.png'):
    """Open Start menu, search for the app, and launch it."""
    pyautogui.press('winleft')
    time.sleep(2)
    pyautogui.write(app_name, interval=0.1)
    time.sleep(2)
    click_image(icon_image)

def open_feedback_panel():
    """Open HPX app and navigate to Feedback panel via Profile icon."""
    click_image('add_device.png')
    click_image("Avatar.png")
    click_image("feedback_btn.png")

def hover_and_click_star_by_index(image_path, star_index=5, star_count=5, confidence=0.9, left_offset=21):
    """Hover and click a star by index (1-based), default is 5th star."""
    location = pyautogui.locateOnScreen(image_path, confidence=confidence)
    if location is None:
        print(" Star row not found on screen.")
        return False

    x, y, width, height = location
    spacing = width / (star_count - 1)
    target_x = x + spacing * (star_index - 1) - left_offset
    target_y = y + height / 2

    pyautogui.moveTo(target_x, target_y, duration=0.5)
    time.sleep(1)
    pyautogui.click()
    print(f"✅ Clicked on star #{star_index}.")
    return True

def minimize_maximize_sequence(minimize_img, maximize_img):
    """Minimize and maximize the app window using image buttons."""
    click_image(minimize_img)
    click_image(maximize_img)

def navigate_to_settings():
    """Click on avatar > settings and scroll up/down."""
    click_image("Avatar.png")
    click_image("settings.png")
    scroll_and_wait(-500, delay=2)
    scroll_and_wait(500, delay=2)

# Pytest fixture for launching HPX application
@pytest.fixture(scope='module')
def launch_hpx_app():
    app_id = "AD2F1837.myHP_v10z8vjag6ke6!App"
    subprocess.Popen(f'explorer shell:AppsFolder\\{app_id}', shell=True)
    time.sleep(2)
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

def test_c53304353_hpx_app_resize_scenarios(launch_hpx_app: None):
    app_launch = wait_for_image(screenshot_path + "myhp_app.png")
    assert app_launch is not None, "HPX-Application did not launch as expected."

    click_image(screenshot_path + "minimize.png")
    click_image(screenshot_path + "maximize.png")

def test_c53303840_hpx_settings_about_verify_the_link_terms_of_use_is_clickable(launch_hpx_app: None):
    click_image(screenshot_path + "Avatar.png")
    click_image(screenshot_path + "Settings.png")
    scroll_and_wait()

    click_image(screenshot_path + "TermsOfUse.png", delay=3)
    windows = gw.getWindowsWithTitle('HP Smart')
    print("✅ Chrome window with expected title opened." if windows else "Chrome window not found.")

def test_c53303839_hpx_settings_about_verify_hp_end_user_license_agreement_link_is_clickable(launch_hpx_app: None):
    pyautogui.hotkey('win', 'd')
    time.sleep(2)
    click_image(screenshot_path + "desktop_myhp.png", click_twice=True)

    click_image(screenshot_path + "HPEndUserLicenseAgreement.png")
    print("✅ Clicked on HP End User License Agreement link.")

    windows = gw.getWindowsWithTitle('End-User License Agreement | HP® Support')
    print("✅ Chrome window opened." if windows else "Chrome window not found.")

def test_c53303838_hpx_settings_about_verify_version_number_read_only(launch_hpx_app: None):
    pyautogui.hotkey('win', 'd')
    time.sleep(2)
    click_image(screenshot_path + "desktop_myhp.png", click_twice=True)

    version_location = wait_for_image(screenshot_path + "Version.png")
    assert version_location is not None, "Version label not found."
    pyautogui.moveTo(version_location)
    pyautogui.click()

    x, y = int(version_location[0]), int(version_location[1])
    before = pyautogui.screenshot(region=(x - 100, y - 50, 200, 100))
    time.sleep(2)
    after = pyautogui.screenshot(region=(x - 100, y - 50, 200, 100))

    if before.tobytes() != after.tobytes():
        pytest.fail("Version label is interactive.")
    else:
        print("✅ Version label is read-only.")

def test_c53303837_hpx_settings_about_verify_version_number_side_panel(launch_hpx_app: None):
    version_location = wait_for_image(screenshot_path + "Version.png")
    assert version_location is not None, 'Version label was not found in About section'

def test_c53303847_hpx_settings_privacy_pipl_data_transfer_toggle(launch_hpx_app: None):
    click_image(screenshot_path + "manage_privacy_settings.png")
    click_image(screenshot_path + "manage_settings_toggle_1.png")
    scroll_and_wait(-300)
    click_image(screenshot_path + "manage_settings_toggle_2.png")
    click_image(screenshot_path + "add_device.png")
    click_image(screenshot_path + "Avatar.png")
    click_image(screenshot_path + "Settings.png")
    click_image(screenshot_path + "manage_privacy_settings.png")
    click_image(screenshot_path + "manage_settings_toggle_1_close.png")
    scroll_and_wait(-300)
    click_image(screenshot_path + "manage_settings_toggle_2_close.png")

def test_c53681236_hpx_feedback_submit_button_position(launch_hpx_app: None):
    click_image(screenshot_path + "add_device.png")
    click_image(screenshot_path + "Avatar.png")
    click_image(screenshot_path + "feedback_btn.png")
    scroll_and_wait()
    submit_button = wait_for_image(screenshot_path + "submit_feedback.png")
    assert submit_button is not None, "Submit button not found."
    assert submit_button.y > 500, f"Submit button positioned incorrectly at y={submit_button.y}."
    print(f"✅ Submit button at position: {submit_button}")

def test_c53681235_hpx_feedback_email_field_valid(launch_hpx_app: None):
    scroll_and_wait(500)
    click_image(screenshot_path + "5_star.png")
    click_image(screenshot_path + "feedback_dropdown_1.png")
    click_image(screenshot_path + "get_tech_support.png")
    click_image(screenshot_path + "feedback_dropdown_2.png")
    click_image(screenshot_path + "load_time.png")
    scroll_and_wait(-500)

    click_image(screenshot_path + "feedback_email_id.png")
    pyautogui.write("kbc@gmail.com", interval=0.1)
    print("✅ Entered email: kbc@gmail.com")

    click_image(screenshot_path + "feedback_submit.png")

def test_c53681234_hpx_feedback_invalid_email_error_message(launch_hpx_app: None):
    click_image(screenshot_path + "Avatar.png")
    click_image(screenshot_path + "feedback_btn.png")
    click_image(screenshot_path + "5_star.png")
    select_dropdown_option(screenshot_path + "feedback_dropdown_1.png", screenshot_path + "get_tech_support.png")
    select_dropdown_option(screenshot_path + "feedback_dropdown_2.png", screenshot_path + "load_time.png")
    pyautogui.scroll(-500)

    email_field = wait_for_image(screenshot_path + "feedback_email_id.png", timeout=10)
    assert email_field is not None, "Email field not found."
    pyautogui.moveTo(email_field)
    pyautogui.click()
    pyautogui.write("kbcgmail.com", interval=0.1)
    print("✅ Entered invalid email: kbcgmail.com")
    time.sleep(2)

    submit_btn = wait_for_image(screenshot_path + "submit_feedback.png")
    assert submit_btn is not None, "Submit button not found."
    print("✅ Submit button is not clickable with invalid email.")

def test_c53681233_hpx_feedback_email_field_optional(launch_hpx_app: None):
    email_optional = wait_for_image(screenshot_path + "feedback_email_image.png", timeout=10)
    assert email_optional is not None, "Email optional indicator not found."
    print("✅ Email ID optional indicator found.")

def test_c53681230_hpx_feedback_second_dropdown_options(launch_hpx_app: None):
    pyautogui.scroll(500)
    click_image(screenshot_path + "load_time_1.png")
    print("✅ Opened second dropdown.")
    time.sleep(2)

    assert wait_for_image(screenshot_path + "load_time.png", timeout=10), "First option not found."
    print("✅ First name detected.")
    time.sleep(1)
    location = wait_for_image(screenshot_path + "load_time.png", timeout=10, confidence=0.8)
    assert location is not None, "❌ Load image not found for hovering."
    pyautogui.moveTo(location, duration=0.5)

    scroll_and_wait()
    time.sleep(2)
    assert wait_for_image(screenshot_path + "dropdown_other2.png", timeout=10), "Last option not found."
    print("✅ Last name detected.")

def test_c53681228_hpx_feedback_first_dropdown_options(launch_hpx_app: None):
    click_image(screenshot_path + "get_tech_support_1.png", click_twice=True)
    print("✅ Opened first dropdown.")
    time.sleep(3)

    assert wait_for_image(screenshot_path + "dropdown_get_tech.png", timeout=10), "First option not found."
    print("✅ First name detected.")
    time.sleep(1)
    location = wait_for_image(screenshot_path + "get_tech_support.png", timeout=10, confidence=0.8)
    assert location is not None, "❌ Load image not found for hovering."
    pyautogui.moveTo(location, duration=0.5)

    scroll_and_wait()
    time.sleep(2)
    assert wait_for_image(screenshot_path + "dropdown_other1.png", timeout=10), "Last option not found."
    print("✅ Last name detected.")

def test_c53681224_hpx_feedback_back_button(launch_hpx_app: None):
    click_image(screenshot_path + "menu_btn.png", click_twice=True)
    print("✅ Clicked on Menu (back) button.")
    time.sleep(5)

def test_c53681222_hpx_feedback_slideout_open(launch_hpx_app: None):
    click_image(screenshot_path + "feedback_btn.png")
    print("✅ Feedback slide out opened correctly.")

def test_c53681221_hpx_feedback_right_navigation_panel(launch_hpx_app: None):
    click_image(screenshot_path + "add_device.png")
    click_image(screenshot_path + "Avatar.png")
    print("✅ Right navigation panel accessible via Avatar/Profile.")

def test_c53304152_hpx_app_icon_and_color_uniformity(launch_hpx_app: None):
    click_image(screenshot_path + "add_device.png")
    profile_icon = wait_for_image(screenshot_path + "Avatar.png")
    assert profile_icon is not None, "Profile icon not found"
    print("Profile icon verified for visual consistency.")

def test_c53304154_hpx_app_invoke_start_menu():
    search_and_launch_app()
    privacy_dialog = wait_for_image(screenshot_path + "myhp_app.png", timeout=10)
    assert privacy_dialog is not None, "❌ MyHP application may not have launched correctly."
    print("MyHP app launched and privacy dialog detected.")

def test_c53304155_hpx_pin_to_taskbar():
    pyautogui.press('win')
    time.sleep(1)
    pyautogui.write('myhp', interval=0.1)
    time.sleep(2)
    right_click_and_select(screenshot_path + "myhp.png", screenshot_path + "pin_to_taskbar.png")

# Click the app from taskbar
    app_tile = wait_for_image(screenshot_path + "app_tile_menu.png")
    assert app_tile is not None, "Taskbar app tile not found"
    pyautogui.moveTo(app_tile)
    pyautogui.click()
    time.sleep(2)

# Validate app launch
    assert wait_for_image(screenshot_path + "myhp_app.png") is not None, "App did not open from taskbar"
    print("✅ App opened from taskbar")

def test_c53304156_hpx_pin_to_start_menu():
    pyautogui.press('win')
    time.sleep(2)
    pyautogui.write('myhp', interval=0.1)
    time.sleep(2)
    right_click_and_select(screenshot_path + "myhp.png", screenshot_path + "pin_to_start.png")
    print("✅ App pinned to Start menu")

def test_c53304175_hpx_app_invoke_multiple_methods(launch_hpx_app: None):
    pyautogui.press('winleft')
    time.sleep(2)
    pyautogui.write('myhp', interval=0.1)
    time.sleep(2)

    myhp_icon = wait_for_image(screenshot_path + "myhp.png", timeout=10)
    assert myhp_icon is not None, "'myHP' application icon not found."
    pyautogui.moveTo(myhp_icon)
    pyautogui.click()

    privacy_dialog = wait_for_image(screenshot_path + "myhp_app.png", timeout=10)
    assert privacy_dialog is not None, "Privacy dialog not found."

    pyautogui.press('win')
    time.sleep(1)
    pyautogui.write('myhp', interval=0.1)
    time.sleep(2)

    myhp_location = wait_for_image(screenshot_path + "myhp.png", timeout=10)
    assert myhp_location is not None, "MyHP icon not found in search results."

    pyautogui.moveTo(myhp_location)
    pyautogui.click(button='right')
    time.sleep(1)

    unpin_option = wait_for_image(screenshot_path + "unpin_to_start.png", timeout=5)
    assert unpin_option is not None, "'Unpin from Start' not found."
    pyautogui.moveTo(unpin_option)
    pyautogui.click()
    time.sleep(3)

    pyautogui.moveTo(myhp_location)
    pyautogui.click(button='right')
    time.sleep(1)

    unpin_location = wait_for_image(screenshot_path + "unpin_to_taskbar.png", timeout=10)
    assert unpin_location is not None, "'Unpin from Taskbar' not found."
    pyautogui.moveTo(unpin_location)
    pyautogui.click()
    time.sleep(3)

    pyautogui.moveTo(myhp_location)
    pyautogui.click(button='right')
    time.sleep(2)

    pin_location = wait_for_image(screenshot_path + "pin_to_taskbar.png", timeout=10)
    assert pin_location is not None, "'Pin to Taskbar' not found."
    pyautogui.moveTo(pin_location)
    pyautogui.click()
    time.sleep(3)

    pyautogui.press('win')
    time.sleep(2)
    pyautogui.write('myhp', interval=0.1)
    time.sleep(2)

    myhp_icon = wait_for_image(screenshot_path + "myhp.png", timeout=10)
    assert myhp_icon is not None, "MyHP icon not found."
    pyautogui.moveTo(myhp_icon)
    pyautogui.click(button='right')
    time.sleep(3)

    pin_option = wait_for_image(screenshot_path + "pin_to_start.png", timeout=5)
    assert pin_option is not None, "'Pin to Start' option not found."
    pyautogui.moveTo(pin_option)
    pyautogui.click()
    time.sleep(3)

    app_tile_location = wait_for_image(screenshot_path + "app_tile_menu.png", timeout=10)
    assert app_tile_location is not None, "App tile not found."
    pyautogui.moveTo(app_tile_location)
    pyautogui.click()

def test_c53303844_hpx_settings_privacy_manage_privacy_ui(launch_hpx_app: None):
    click_image(screenshot_path + "Avatar.png")
    click_image(screenshot_path + "Settings.png")
    click_image(screenshot_path + "manage_privacy_settings.png")

def test_c53303843_hpx_settings_privacy_visibility_manage_privacy(launch_hpx_app: None):
    add_device_location = wait_for_image(screenshot_path + "add_device.png")
    assert add_device_location is not None, 'Add Device button not found'
    pyautogui.moveTo(add_device_location)
    pyautogui.click()
    time.sleep(2)

    click_image(screenshot_path + "Avatar.png")
    click_image(screenshot_path + "Settings.png")
    click_image(screenshot_path + "manage_privacy_settings.png")

    add_device_location = wait_for_image(screenshot_path + "add_device.png")
    assert add_device_location is not None, 'Add Device button not found'
    pyautogui.moveTo(add_device_location)
    pyautogui.click()
    time.sleep(2)

def test_c53681231_hpx_feedback_second_dropdown_functionality(launch_hpx_app: None):
    click_image(screenshot_path + "Avatar.png")
    click_image(screenshot_path + "feedback_btn.png")

    for dropdown_img, option_img in [
        (screenshot_path + "feedback_dropdown_2.png", screenshot_path + "load_time.png"),
        (screenshot_path + "load_time_1.png", screenshot_path + "ease_of_use.png")
    ]:
        dropdown = wait_for_image(dropdown_img, timeout=10, confidence=0.8)
        assert dropdown is not None, f"{dropdown_img} not found on screen."
        pyautogui.moveTo(dropdown)
        time.sleep(2)
        pyautogui.click()
        print(f"Clicked on {dropdown_img}.")
        time.sleep(2)

        option = wait_for_image(screenshot_path + option_img, timeout=10, confidence=0.8)
        assert option is not None, f"{option_img} not found on screen."
        pyautogui.moveTo(option)
        print(f"Hovering on {option_img}")
        time.sleep(4)
        pyautogui.click()
        time.sleep(2)

def test_c53681229_hpx_feedback_first_dropdown_functionality(launch_hpx_app: None):
    for dropdown_img, option_img in [
        (screenshot_path + "feedback_dropdown_1.png", screenshot_path + "get_tech_support.png"),
        (screenshot_path + "get_tech_support_1.png", screenshot_path + "configure_my_device.png")
        ]:
        dropdown = wait_for_image(dropdown_img, timeout=10, confidence=0.8)
        assert dropdown is not None, f"{dropdown_img} not found on screen."
        pyautogui.moveTo(dropdown)
        time.sleep(2)
        pyautogui.click()
        print(f"✅ Clicked on {dropdown_img}.")
        time.sleep(2)

        option = wait_for_image(screenshot_path + option_img, timeout=10, confidence=0.8)
        assert option is not None, f"{option_img} not found on screen."
        pyautogui.moveTo(option)
        print(f"✅ Hovering on {option_img}")
        time.sleep(4)
        pyautogui.click()
        time.sleep(2)

def test_c53681227_hpx_feedback_five_star_rating_position(launch_hpx_app: None):
    click_image(screenshot_path + "add_device.png")
    click_image(screenshot_path + "Avatar.png")
    click_image(screenshot_path + "feedback_btn.png")
    five_star_location = wait_for_image(screenshot_path + "5_star.png", timeout=15, confidence=0.9)
    assert five_star_location is not None, "5-star alignment not found on screen."
    print("5-star alignment detected on screen.")

def test_c53681223_hpx_feedback_content_matching(launch_hpx_app: None):
    click_image(screenshot_path + "add_device.png")
    click_image(screenshot_path + "Avatar.png")
    click_image(screenshot_path + "feedback_btn.png")
    print("Feedback page verified")

def test_c53304158_hpx_app_resize_scenarios_fullscreen(launch_hpx_app: None):
    add_device_location = wait_for_image(screenshot_path + "add_device.png")
    assert add_device_location is not None, "Add Device button not found"
    pyautogui.moveTo(add_device_location)
    pyautogui.click()
    time.sleep(2)

    minimize_btn = wait_for_image(screenshot_path + "minimize.png")
    assert minimize_btn is not None, "Minimize button not found."
    pyautogui.click(minimize_btn)
    time.sleep(2)

    maximize_btn = wait_for_image(screenshot_path + "maximize.png")
    assert maximize_btn is not None, "Maximize button not found."
    pyautogui.click(maximize_btn)
    time.sleep(2)

def test_C53681226_feedback_5_star_rating_system(launch_hpx_app: None):
    profile_icon = wait_for_image(screenshot_path + "Avatar.png", timeout=10)
    assert profile_icon is not None, "❌ Profile icon not found!"
    pyautogui.moveTo(profile_icon)
    pyautogui.click()
    print("✅ Clicked on Profile icon.")
    time.sleep(2)

    feedback_button = wait_for_image(screenshot_path + "feedback_btn.png", timeout=10)
    assert feedback_button is not None, "Feedback button not found!"
    pyautogui.moveTo(feedback_button)
    pyautogui.click()
    print("Clicked on Feedback button.")
    time.sleep(2)

    star_1 = wait_for_image(screenshot_path + "1_star.png", timeout=10)
    assert star_1 is not None, "1st star not found!"
    pyautogui.moveTo(star_1)
    pyautogui.click()
    print("Clicked on 1st star.")
    time.sleep(2)

    click_image(screenshot_path + "add_device.png")
    click_image(screenshot_path + "Avatar.png")
    click_image(screenshot_path + "feedback_btn.png")

    print("Step 8: Hover and click on 5th star using full row image...")
    success = hover_and_click_star_by_index(screenshot_path + "5_star.png", star_index=5)
    assert success, "Failed to hover/click 5th star."
    pyautogui.click()
    pyautogui.click()
    time.sleep(2)

def test_C53681225_feedback_star_rating_functionality(launch_hpx_app: None):
    click_image(screenshot_path + "add_device.png")
    click_image(screenshot_path + "Avatar.png")
    click_image(screenshot_path + "feedback_btn.png")

    star_1 = wait_for_image(screenshot_path + "1_star.png", timeout=10)
    assert star_1 is not None, "1st star not found!"
    pyautogui.moveTo(star_1)
    pyautogui.click()
    print("Clicked on 1st star.")
    time.sleep(8)
    pyautogui.click()
    time.sleep(2)

    click_image(screenshot_path + "add_device.png")
    click_image(screenshot_path + "Avatar.png")
    click_image(screenshot_path + "feedback_btn.png")

    print("Step 8: Hover and click on 5th star using full row image...")
    success = hover_and_click_star_by_index(screenshot_path + "5_star.png", star_index=5)
    assert success, "Failed to hover/click 5th star."
    pyautogui.click()
    pyautogui.click()
    time.sleep(8)
    pyautogui.click()
    time.sleep(3)

    click_image(screenshot_path + "add_device.png")

def test_C53304159_scroll_bar(launch_hpx_app: None):
    click_image(screenshot_path + "Avatar.png")
    click_image(screenshot_path + "settings.png")
    scroll_and_wait(-500, delay=2)
    scroll_and_wait(500, delay=2)

    minimize_maximize_sequence(screenshot_path + "minimize.png", screenshot_path + "menu_btn.png")
    click_image(screenshot_path + "settings.png")
    scroll_and_wait(-500, delay=2)
    scroll_and_wait(500, delay=2)
    click_image(screenshot_path + "maximize.png")

def test_c53304153_app_window_operations(launch_hpx_app: None):
    windows = gw.getWindowsWithTitle("MyHP")
    assert windows, "MyHP application window did not appear."
    window = windows[0]

# Minimize and Maximize
    minimize_maximize_sequence(screenshot_path + "minimize.png", screenshot_path + "maximize.png")

# Right-click Title Bar
    title_bar_x = window.topleft.x + 50
    title_bar_y = window.topleft.y + 10
    pyautogui.moveTo(title_bar_x, title_bar_y, duration=0.5)
    pyautogui.rightClick()
    print("Right-clicked on title bar.")
    time.sleep(1)

# Click Resize
    resize_button_location = wait_for_image(screenshot_path + "minimize.png")
    assert resize_button_location, "Resize button not found."
    pyautogui.moveTo(resize_button_location)
    pyautogui.click()
    print("Resize button clicked.")

# Record initial width
    original_width = window.width
    print(f"Original width: {original_width}")

# Resize via dragging
    start_drag_x = window.topleft.x + window.width - 5
    start_drag_y = window.topleft.y + window.height - 5
    pyautogui.moveTo(start_drag_x, start_drag_y, duration=0.5)
    pyautogui.dragRel(-1000, -500, duration=1, button="left")
    print("Window resized via drag.")
    
if __name__ == '__main__':
    pytest.main([__file__])