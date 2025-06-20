import time
import pyautogui
import subprocess
import pytest
import pygetwindow as gw

# Constants
screenshot_path = 'screenshot/karthik_dark_mode/'
username = 'karthik.m@ascendion.com'
password = '262202@Km'

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
    yield # This allows the test to run, and you can add teardown here if needed

# Function to activate Chrome window
def activate_chrome_window():
    # Wait for Chrome to open and detect the correct window
    logger.info("Activating Chrome window")
    for _ in range(10):
        windows = gw.getWindowsWithTitle('HP account')
        if windows:
            chrome_window = windows[0]
            chrome_window.activate()
            return True
        time.sleep(1)
    print("Chrome window not found.")
    return False

# Function to login to the HP account
def login_hp_account():
    logger.info("Logging in to HP account")
    if not activate_chrome_window():
        return
    time.sleep(10)  # Wait for page to fully load
    username_or_email_address_textbox = wait_for_image(screenshot_path + "username_or_email_address_textbox.png")
    assert username_or_email_address_textbox is not None, "Username or email address textbox not found"
    pyautogui.click(username_or_email_address_textbox)
    pyautogui.write(username)
    pyautogui.press('tab', 2)  # Press tab twice to navigate to password field
    pyautogui.press('enter')
    time.sleep(5)
    passwword_text_box = wait_for_image(screenshot_path + "passwword_text_box.png")
    assert passwword_text_box is not None, "Password text box not found"
    pyautogui.click(passwword_text_box)
    pyautogui.write(password, interval=0.1)  # Type password with a slight delay
    pyautogui.press('tab', 2)
    pyautogui.press('enter')  # Submit
    time.sleep(15)  # Wait for sign-in to complete

# Function to logout of the HP account
def logout_hp_account():
    logger.info("Logging out of HP account")
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



# Test case C53681238
@pytest.mark.usefixtures("launch_hpx_app")
def test__c53681238_general_feedback_verify_a_confirmation_message_is_displayed_upon_submitting_the_feedback_form():
    click_image(screenshot_path + "avatar.png")
    time.sleep(2)
    click_image(screenshot_path + "feedback_button.png")
    time.sleep(2)
    rating_value = 5
    star_image = f"{rating_value}_star.png"
    click_image(screenshot_path + star_image)
    time.sleep(2)
    select_dropdown_option(screenshot_path + "feedback_dropdown_1.png", screenshot_path + "get_tech_support.png")
    select_dropdown_option(screenshot_path + "feedback_dropdown_2.png", screenshot_path + "load_time.png")
    pyautogui.scroll(-500)

    email_field = wait_for_image(screenshot_path + "feedback_email_id.png", timeout=10)
    assert email_field is not None, "Email field not found."
    pyautogui.moveTo(email_field)
    pyautogui.click()
    pyautogui.write("kbc@gmail.com", interval=0.1)
    time.sleep(2)

    submit_btn = wait_for_image(screenshot_path + "submit_feedback.png")
    assert submit_btn is not None, "Submit button not found."
    print("✅ Submit button is not clickable with invalid email.")
    pyautogui.moveTo(submit_btn)
    pyautogui.click()
    time.sleep(2)

    pyautogui.scroll(500)
    time.sleep(10)
    if rating_value >= 5:
        feedback_msg = wait_for_image(screenshot_path + "positive_feedback_msg.png", timeout=20)
        assert feedback_msg is not None, "Positive feedback message not displayed."
        print("✅ Thanks for your feedback. It's great to know you are enjoying our app.")
    else:
        feedback_msg = wait_for_image(screenshot_path + "negative_feedback_msg.png", timeout=20)
        assert feedback_msg is not None, "Constructive feedback message not displayed."
        print("✅ We appreciate your feedback and will use it to improve our app.")
    click_image(screenshot_path + "menu_button.png")
    time.sleep(2)
    click_on_close_button()


# Test case C53681237
@pytest.mark.usefixtures("launch_hpx_app")
def test__c53681237_general_feedback_verify_feedback_form_submission_after_clicking_submit_button():
    click_image(screenshot_path + "avatar.png")
    click_image(screenshot_path + "feedback_button.png")
    rating_value = 5
    star_image = f"{rating_value}_star.png"
    click_image(screenshot_path + star_image)
    time.sleep(2)
    select_dropdown_option(screenshot_path + "feedback_dropdown_1.png", screenshot_path + "get_tech_support.png")
    select_dropdown_option(screenshot_path + "feedback_dropdown_2.png", screenshot_path + "load_time.png")
    pyautogui.scroll(-500)

    email_field = wait_for_image(screenshot_path + "feedback_email_id.png", timeout=10)
    assert email_field is not None, "Email field not found."
    pyautogui.moveTo(email_field)
    pyautogui.click()
    pyautogui.write("kbc@gmail.com", interval=0.1)
    time.sleep(2)

    submit_btn = wait_for_image(screenshot_path + "submit_feedback.png")
    assert submit_btn is not None, "Submit button not found."
    print("✅ Submit button is not clickable with invalid email.")
    pyautogui.moveTo(submit_btn)
    pyautogui.click()
    time.sleep(2)

    pyautogui.scroll(500)
    time.sleep(10)
    if rating_value >= 4:
        feedback_msg = wait_for_image(screenshot_path + "positive_feedback_msg.png", timeout=10)
        assert feedback_msg is not None, "Positive feedback message not displayed."
        print("✅ Thanks for your feedback. It's great to know you are enjoying our app.")
    else:
        feedback_msg = wait_for_image(screenshot_path + "negative_feedback_msg.png", timeout=10)
        assert feedback_msg is not None, "Constructive feedback message not displayed."
        print("✅ We appreciate your feedback and will use it to improve our app.")
    click_image(screenshot_path + "menu_button.png")
    time.sleep(2)
    click_on_close_button()


# Test case C53681236
def test__c53681236_general_feedback_verify_submit_button_alignment_on_feedback_slideout(launch_hpx_app):
    click_image(screenshot_path + "avatar.png")
    click_image(screenshot_path + "feedback_button.png")
    click_image(screenshot_path + "3_star.png")
    select_dropdown_option(screenshot_path + "feedback_dropdown_1.png", screenshot_path + "get_tech_support.png")
    select_dropdown_option(screenshot_path + "feedback_dropdown_2.png", screenshot_path + "load_time.png")
    pyautogui.scroll(-500)

    email_field = wait_for_image(screenshot_path + "feedback_email_id.png", timeout=10)
    assert email_field is not None, "Email field not found."
    pyautogui.moveTo(email_field)
    pyautogui.click()
    pyautogui.write("kbc@gmail.com", interval=0.1)
    time.sleep(2)

    submit_btn = wait_for_image(screenshot_path + "submit_feedback.png")
    assert submit_btn is not None, "Submit button not found."
    print("✅ Submit button on the feedback slideout screen.")
    pyautogui.moveTo(submit_btn)
    pyautogui.click()
    time.sleep(2)
    pyautogui.scroll(500)
    time.sleep(10)

    click_image(screenshot_path + "menu_button.png")
    print("✅ Clicked on Menu (back) button.")
    time.sleep(2)
    click_on_close_button()

# Test case C53681235
def test_c53681235_general_feedback_verify_email_field_accepts_valid_email(launch_hpx_app):
    click_image(screenshot_path + "avatar.png")
    click_image(screenshot_path + "feedback_button.png")
    rating_value = 3
    star_image = f"{rating_value}_star.png"
    click_image(screenshot_path + star_image)
    time.sleep(2)
    select_dropdown_option(screenshot_path + "feedback_dropdown_1.png", screenshot_path + "get_tech_support.png")
    select_dropdown_option(screenshot_path + "feedback_dropdown_2.png", screenshot_path + "load_time.png")
    pyautogui.scroll(-500)

    email_field = wait_for_image(screenshot_path + "feedback_email_id.png", timeout=10)
    assert email_field is not None, "Email field not found."
    pyautogui.moveTo(email_field)
    pyautogui.click()
    pyautogui.write("kbc@gmail.com", interval=0.1)
    time.sleep(2)

    submit_btn = wait_for_image(screenshot_path + "submit_feedback.png")
    assert submit_btn is not None, "Submit button not found."
    print("✅ Email should correctly capture the address without errors.")
    pyautogui.moveTo(submit_btn)
    pyautogui.click()
    time.sleep(2)

    pyautogui.scroll(500)
    time.sleep(5)
    click_image(screenshot_path + "menu_button.png")
    time.sleep(2)
    click_on_close_button()


# Test case C53681234
def test__c53681234_general_feedback_verify_invalid_email_error_message(launch_hpx_app):
    click_image(screenshot_path + "avatar.png")
    time.sleep(2)
    click_image(screenshot_path + "feedback_button.png")
    time.sleep(2)
    rating_value = 3
    star_image = f"{rating_value}_star.png"
    click_image(screenshot_path + star_image)
    time.sleep(2)
    select_dropdown_option(screenshot_path + "feedback_dropdown_1.png", screenshot_path + "get_tech_support.png")
    select_dropdown_option(screenshot_path + "feedback_dropdown_2.png", screenshot_path + "load_time.png")
    pyautogui.scroll(-500)

    email_field = wait_for_image(screenshot_path + "feedback_email_id.png", timeout=10)
    assert email_field is not None, "Email field not found."
    pyautogui.moveTo(email_field)
    pyautogui.click()
    pyautogui.write("karc.com", interval=0.1)
    print("✅ Entered invalid email: karc.com")
    time.sleep(2)
    invalid_email = wait_for_image(screenshot_path + 'invalid_email.png', timeout=10, confidence=0.8)
    assert invalid_email is not None, "HPx application did not launch."
    pyautogui.moveTo(invalid_email)
    pyautogui.click()
    time.sleep(2)

    error_msg = wait_for_image(screenshot_path + 'email_error_msg.png', timeout=10, confidence=0.8)
    assert error_msg is not None, "Top App Bar icons are not visible."
    pyautogui.moveTo(error_msg)
    print("You Entered invalid email: karc.com")

    time.sleep(2)

    pyautogui.scroll(500)
    time.sleep(5)

    click_image(screenshot_path + "menu_button.png")
    time.sleep(2)
    click_on_close_button()



# Test case C53681233
def test__c53681233_general_feedback_verify_email_field_is_optional():
    click_image(screenshot_path + "avatar.png")
    click_image(screenshot_path + "feedback_button.png")
    rating_value = 3
    star_image = f"{rating_value}_star.png"
    click_image(screenshot_path + star_image)
    time.sleep(2)
    select_dropdown_option(screenshot_path + "feedback_dropdown_1.png", screenshot_path + "get_tech_support.png")
    select_dropdown_option(screenshot_path + "feedback_dropdown_2.png", screenshot_path + "load_time.png")
    pyautogui.scroll(-500)

    feedback_message = wait_for_image(screenshot_path + "feedback_msg.png", timeout=10)
    assert feedback_message is not None, "Feedback message field not found."
    pyautogui.moveTo(feedback_message)
    pyautogui.click()
    pyautogui.write("Like HP", interval=0.1)
    time.sleep(2)

    email_field = wait_for_image(screenshot_path + "feedback_email_id.png", timeout=10)
    assert email_field is not None, "Email field not found."
    pyautogui.moveTo(email_field)
    print("✅ Email address field is optional.")


    submit_btn = wait_for_image(screenshot_path + "submit_feedback.png")
    assert submit_btn is not None, "Submit button not found."
    pyautogui.moveTo(submit_btn)
    pyautogui.click()
    time.sleep(2)

    pyautogui.scroll(500)
    time.sleep(5)
    click_image(screenshot_path + "menu_button.png")
    time.sleep(2)
    click_on_close_button()


# Test case C53681232
def test__c53681232_general_feedback_verify_text_box_accepts_and_displays_input():
    click_image(screenshot_path + "avatar.png")
    click_image(screenshot_path + "feedback_button.png")
    rating_value = 3
    star_image = f"{rating_value}_star.png"
    click_image(screenshot_path + star_image)
    time.sleep(2)
    select_dropdown_option(screenshot_path + "feedback_dropdown_1.png", screenshot_path + "get_tech_support.png")
    select_dropdown_option(screenshot_path + "feedback_dropdown_2.png", screenshot_path + "load_time.png")
    pyautogui.scroll(-500)

    feedback_message = wait_for_image(screenshot_path + "feedback_msg.png", timeout=10)
    assert feedback_message is not None, "Feedback message field not found."
    pyautogui.moveTo(feedback_message)
    pyautogui.click()
    pyautogui.write("This is a feedback test. \nIt includes special characters like !@#$%^&*() and line breaks." 
                          "We are testing if the feedback text box correctly displays long strings, special characters, and line breaks."
                          "Let's add some more text to hit the character limit.", interval=0.1)
    time.sleep(2)

    submit_btn = wait_for_image(screenshot_path + "submit_feedback.png")
    assert submit_btn is not None, "Submit button not found."
    pyautogui.moveTo(submit_btn)
    pyautogui.click()
    print("✅ Email address field is optional.")
    time.sleep(2)

    pyautogui.scroll(500)
    time.sleep(5)
    click_image(screenshot_path + "menu_button.png")
    time.sleep(2)
    click_on_close_button()


# Test case C53681231
def test__c53681231_general_feedback_verify_functionality_of_second_dropdown_menu():
    click_image(screenshot_path + "avatar.png")
    click_image(screenshot_path + "feedback_button.png")
    click_image(screenshot_path + "3_star.png")
    select_dropdown_option(screenshot_path + "feedback_dropdown_1.png", screenshot_path + "configure_my_device.png")
    select_dropdown_option(screenshot_path + "feedback_dropdown_2.png", screenshot_path + "ease_of_use.png")
    pyautogui.scroll(-500)

    email_field = wait_for_image(screenshot_path + "feedback_email_id.png", timeout=10)
    assert email_field is not None, "Email field not found."
    pyautogui.moveTo(email_field)
    pyautogui.click()
    pyautogui.write("kbc@gmail.com", interval=0.1)
    time.sleep(2)

    submit_btn = wait_for_image(screenshot_path + "submit_feedback.png")
    assert submit_btn is not None, "Submit button not found."
    print("✅ Submit button on the feedback slideout screen.")
    pyautogui.moveTo(submit_btn)
    pyautogui.click()
    time.sleep(2)
    pyautogui.scroll(500)
    time.sleep(10)

    click_image(screenshot_path + "menu_button.png")
    print("✅ Clicked on Menu (back) button.")
    time.sleep(2)
    click_on_close_button()







# Test case C53681230
def test_c53681230_hpx_feedback_second_dropdown_options(launch_hpx_app: None):
    click_image(screenshot_path + "avatar.png")
    click_image(screenshot_path + "feedback_button.png")
    click_image(screenshot_path + "3_star.png")
    select_dropdown_option(screenshot_path + "feedback_dropdown_1.png", screenshot_path + "configure_my_device.png")
    select_dropdown_option(screenshot_path + "feedback_dropdown_2.png", screenshot_path + "ease_of_use.png")
    pyautogui.scroll(-500)

    email_field = wait_for_image(screenshot_path + "feedback_email_id.png", timeout=10)
    assert email_field is not None, "Email field not found."
    pyautogui.moveTo(email_field)
    pyautogui.click()
    pyautogui.write("kbc@gmail.com", interval=0.1)
    time.sleep(2)

    submit_btn = wait_for_image(screenshot_path + "submit_feedback.png")
    assert submit_btn is not None, "Submit button not found."
    print("✅ Submit button on the feedback slideout screen.")
    pyautogui.moveTo(submit_btn)
    pyautogui.click()
    time.sleep(2)
    pyautogui.scroll(500)
    time.sleep(10)

    click_image(screenshot_path + "menu_button.png")
    print("✅ Clicked on Menu (back) button.")
    time.sleep(2)
    click_on_close_button()

# Test case C53681229
def test__C53681229_general_feedback_verify_functionality_of_first_dropdown_menu():
    click_image(screenshot_path + "avatar.png")
    click_image(screenshot_path + "feedback_button.png")
    click_image(screenshot_path + "3_star.png")
    select_dropdown_option(screenshot_path + "feedback_dropdown_1.png", screenshot_path + "get_tech_support.png")
    select_dropdown_option(screenshot_path + "feedback_dropdown_2.png", screenshot_path + "load_time.png")
    pyautogui.scroll(-500)

    email_field = wait_for_image(screenshot_path + "feedback_email_id.png", timeout=10)
    assert email_field is not None, "Email field not found."
    pyautogui.moveTo(email_field)
    pyautogui.click()
    pyautogui.write("kbc@gmail.com", interval=0.1)
    time.sleep(2)

    submit_btn = wait_for_image(screenshot_path + "submit_feedback.png")
    assert submit_btn is not None, "Submit button not found."
    print("✅ Submit button on the feedback slideout screen.")
    pyautogui.moveTo(submit_btn)
    pyautogui.click()
    time.sleep(2)
    pyautogui.scroll(500)
    time.sleep(10)

    click_image(screenshot_path + "menu_button.png")
    print("✅ Clicked on Menu (back) button.")
    time.sleep(2)
    click_on_close_button()



# Test case C53681228
def test__C53681228_general_feedback_verify_options_in_first_dropdown_menu():
    click_image(screenshot_path + "avatar.png")
    click_image(screenshot_path + "feedback_button.png")
    click_image(screenshot_path + "3_star.png")
    select_dropdown_option(screenshot_path + "feedback_dropdown_1.png", screenshot_path + "get_tech_support.png")
    select_dropdown_option(screenshot_path + "feedback_dropdown_2.png", screenshot_path + "load_time.png")
    pyautogui.scroll(-500)

    email_field = wait_for_image(screenshot_path + "feedback_email_id.png", timeout=10)
    assert email_field is not None, "Email field not found."
    pyautogui.moveTo(email_field)
    pyautogui.click()
    pyautogui.write("kbc@gmail.com", interval=0.1)
    time.sleep(2)

    submit_btn = wait_for_image(screenshot_path + "submit_feedback.png")
    assert submit_btn is not None, "Submit button not found."
    print("✅ Submit button on the feedback slideout screen.")
    pyautogui.moveTo(submit_btn)
    pyautogui.click()
    time.sleep(2)
    pyautogui.scroll(500)
    time.sleep(10)

    click_image(screenshot_path + "menu_button.png")
    print("✅ Clicked on Menu (back) button.")
    time.sleep(2)
    click_on_close_button()    

# Test case C53681227
def test__C53681227_general_feedback_verify_five_star_rating_position(launch_hpx_app):
    # click_image(screenshot_path + "add_device.png")
    click_image(screenshot_path + "avatar.png")
    click_image(screenshot_path + "feedback_button.png")
    five_star_location = wait_for_image(screenshot_path + "5_star.png", timeout=15, confidence=0.9)
    assert five_star_location is not None, "5-star alignment not found on screen."
    pyautogui.moveTo(five_star_location)
    pyautogui.click()
    print("5-star alignment detected on screen.")
    time.sleep(1)
    select_dropdown_option(screenshot_path + "feedback_dropdown_1.png", screenshot_path + "get_tech_support.png")
    select_dropdown_option(screenshot_path + "feedback_dropdown_2.png", screenshot_path + "load_time.png")
    pyautogui.scroll(-500)

    email_field = wait_for_image(screenshot_path + "feedback_email_id.png", timeout=10)
    assert email_field is not None, "Email field not found."
    pyautogui.moveTo(email_field)
    pyautogui.click()
    pyautogui.write("kbc@gmail.com", interval=0.1)
    time.sleep(2)

    submit_btn = wait_for_image(screenshot_path + "submit_feedback.png")
    assert submit_btn is not None, "Submit button not found."
    print("✅ Submit button on the feedback slideout screen.")
    pyautogui.moveTo(submit_btn)
    pyautogui.click()
    time.sleep(2)
    pyautogui.scroll(500)
    time.sleep(10)

    click_image(screenshot_path + "menu_button.png")
    print("✅ Clicked on Menu (back) button.")
    time.sleep(2)
    click_on_close_button()



# Test case C53681226
def test_C53681226_feedback_5_star_rating_system(launch_hpx_app):
    profile_icon = wait_for_image(screenshot_path + "avatar.png", timeout=10)
    assert profile_icon is not None, "❌ Profile icon not found!"
    pyautogui.moveTo(profile_icon)
    pyautogui.click()
    print("✅ Clicked on Profile icon.")
    time.sleep(2)

    feedback_button = wait_for_image(screenshot_path + "feedback_button.png", timeout=10)
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

    # click_image(screenshot_path + "add_device.png")
    # click_image(screenshot_path + "avatar.png")
    # click_image(screenshot_path + "feedback_button.png")

    print("Step 8: Hover and click on 5th star using full row image...")
    success = hover_and_click_star_by_index(screenshot_path + "5_star.png", star_index=5)
    assert success, "Failed to hover/click 5th star."
    pyautogui.click()
    pyautogui.click()
    time.sleep(2)
    click_on_close_button()


def test_C53681225_feedback_star_rating_functionality(launch_hpx_app: None):
    
    click_image(screenshot_path + "avatar.png")
    click_image(screenshot_path + "feedback_button.png")

    star_1 = wait_for_image(screenshot_path + "1_star.png", timeout=10)
    assert star_1 is not None, "1st star not found!"
    pyautogui.moveTo(star_1)
    pyautogui.click()
    print("Clicked on 1st star.")
    time.sleep(8)
    pyautogui.click()
    time.sleep(2)

    # click_image(screenshot_path + "add_device.png")
    # click_image(screenshot_path + "Avatar.png")
    # click_image(screenshot_path + "feedback_btn.png")

    print("Step 8: Hover and click on 5th star using full row image...")
    success = hover_and_click_star_by_index(screenshot_path + "5_star.png", star_index=5)
    assert success, "Failed to hover/click 5th star."
    pyautogui.click()
    pyautogui.click()
    time.sleep(8)
    pyautogui.click()
    time.sleep(3)

    click_on_close_button()


# Test case C53681224
def test__c53681224_general_feedback_verify_back_button_on_feedback_slideout(launch_hpx_app):
    click_image(screenshot_path + "avatar.png")
    click_image(screenshot_path + "feedback_button.png")
    time.sleep(2)
    click_image(screenshot_path + "menu_button.png")
    print("✅ Clicked on Menu (back) button.")
    time.sleep(2)
    click_on_close_button()


# Test case C53681223
def test__c53681223_general_feedback_verify_feedback_content_matches(launch_hpx_app):
    click_image(screenshot_path + "profile_icon.png")
    click_image(screenshot_path + "feedback_button.png")
    print("Feedback content panel verified")
    time.sleep(2)
    click_image(screenshot_path + "menu_button.png")
    print("✅ Clicked on Menu (back) button.")
    time.sleep(2)
    click_on_close_button()


# Test case C53681222
def test__c53681222_general_feedback_verify_feedback_slideout_opens_correctly(launch_hpx_app):
    click_image(screenshot_path + "avatar.png")
    feedback_icon = wait_for_image(screenshot_path + "feedback_button.png")
    assert feedback_icon is not None, "Profile icon not found for hover action"
    pyautogui.moveTo(feedback_icon)
    print("Click on the feedback button")
    time.sleep(2)
    pyautogui.click(feedback_icon)
    time.sleep(2)
    click_on_close_button()


# Test case C53681221
def test__c53681221_general_feedback_verify_right_navigation_panel_accessible_through_profile(launch_hpx_app):
    click_image(screenshot_path + "avatar.png")
    print("Profile button/Avatar found on Home screen")
    time.sleep(2)
    click_on_close_button()


# Test case C53681220
def test__c53681220_general_feedback_verify_feedback_accessible_through_panel_navigation(launch_hpx_app):
    click_image(screenshot_path + "avatar.png")
    feedback_icon = wait_for_image(screenshot_path + "feedback_button.png")
    assert feedback_icon is not None, "Profile icon not found for hover action"
    pyautogui.moveTo(feedback_icon)
    print("Feedback button is Available")
    time.sleep(2)
    click_on_close_button()


if __name__ == '__main__':
    pytest.main([__file__])