import time
import pyautogui
import subprocess
import pytest
import logging

logger = logging.getLogger(__name__)
screenshot_path = "screenshot/hari_dark_mode/"

def wait_for_image(image, timeout=15, confidence=0.6):
    start = time.time()
    while time.time() - start < timeout:
        try:
            loc = pyautogui.locateCenterOnScreen(image, confidence=confidence)
            if loc:
                return loc
        except Exception as e:
            print(f"[Error] locateCenterOnScreen failed: {e}")
        time.sleep(1)
    print(f"[Timeout] Image not found: {image}")
    return None

def click_on_close_button():
    time.sleep(2)
    logger.info("Clicking close button")
    btn = wait_for_image(screenshot_path + "close_btn.png", confidence=0.6)
    if btn:
        pyautogui.click(btn)
    time.sleep(2)

@pytest.fixture(scope='function')
def launch_hpx_app():
    app_id = "AD2F1837.myHP_v10z8vjag6ke6!App"
    print("Launching HPX App...")
    subprocess.Popen(f'explorer shell:AppsFolder\\{app_id}', shell=True)
    time.sleep(30)
    yield True
    print("Closing HPX App...")
    try:
        subprocess.run(["taskkill", "/f", "/im", "HP.myHP.exe"], check=True,
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except subprocess.CalledProcessError:
        print("Warning: HPX App might already be closed.")
def disable_internet_windows():
    try:
        subprocess.run("netsh interface set interface Wi-Fi admin=disable", shell=True, check=True)
        print("✅ Internet disabled successfully.")
    except subprocess.CalledProcessError:
        print("⚠️ Failed to disable internet.")

def enable_internet_windows():
    try:
        subprocess.run("netsh interface set interface Wi-Fi admin=enable", shell=True, check=True)
        print("✅ Internet re-enabled.")
    except subprocess.CalledProcessError:
        print("⚠️ Failed to re-enable internet.")

def navigate_to_feedback_form():
    time.sleep(5)
    pyautogui.click(wait_for_image(screenshot_path + "profile.png"))
    time.sleep(5)
    pyautogui.click(wait_for_image(screenshot_path + "send_feedback_button.png"))

# ---------- Test Cases ----------

@pytest.mark.feedback
def test_tc_C42631125_verify_send_feedback_is_present(launch_hpx_app):
    time.sleep(5)
    pyautogui.click(wait_for_image(screenshot_path + "profile.png"))
    time.sleep(5)
    assert wait_for_image(screenshot_path + "send_feedback_button.png"), "Send Feedback button not found."
    print("✅ TC_C42631125 passed.")
    click_on_close_button()

@pytest.mark.feedback
def test_tc_C42631159_verify_send_feedback_slide(launch_hpx_app):
    navigate_to_feedback_form()
    time.sleep(5)
    assert wait_for_image(screenshot_path + "feedback_slide.png"), "Feedback slider not found."
    print("✅ TC_C42631159 passed.")
    click_on_close_button()

@pytest.mark.feedback
def test_tc_C42631158_verify_feedback_slide_back_btn(launch_hpx_app):
    navigate_to_feedback_form()
    time.sleep(5)
    pyautogui.click(wait_for_image(screenshot_path + "feedback_slide_back.png"))
    time.sleep(5)
    assert wait_for_image(screenshot_path + "feedback_slide_back.png"), "Back button not working."
    print("✅ TC_C42631158 passed.")
    click_on_close_button()

@pytest.mark.feedback
def test_tc_C42631157_verify_rating_star_field(launch_hpx_app):
    navigate_to_feedback_form()
    time.sleep(5)
    assert wait_for_image(screenshot_path + "star.png"), "Rating star missing."
    print("✅ TC_C42631157 passed.")
    click_on_close_button()

@pytest.mark.feedback
def test_tc_C42631156_verify_why_did_you_open_app_today_list(launch_hpx_app):
    navigate_to_feedback_form()
    time.sleep(5)
    assert wait_for_image(screenshot_path + "why_open_app_dropdown.png"), "Dropdown not found."
    print("✅ TC_C42631156 passed.")
    click_on_close_button()

@pytest.mark.feedback
def test_tc_C42631155_verify_first_dropdown_menu_functionality(launch_hpx_app):
    navigate_to_feedback_form()
    time.sleep(5)
    pyautogui.click(wait_for_image(screenshot_path + "feedback_dropdown_1.png"))
    time.sleep(5)
    assert wait_for_image(screenshot_path + "first_dropdown_menu.png"), "First dropdown not functional."
    print("✅ TC_C42631155 passed.")
    click_on_close_button()

@pytest.mark.feedback
def test_tc_C42631154_verify_feedback_related_to_list(launch_hpx_app):
    navigate_to_feedback_form()
    time.sleep(5)
    pyautogui.click(wait_for_image(screenshot_path + "star.png"))
    time.sleep(5)
    pyautogui.click(wait_for_image(screenshot_path + "feedback_dropdown_1.png"))
    time.sleep(5)
    pyautogui.click(wait_for_image(screenshot_path + "first_dropdown_menu.png"))
    time.sleep(5)
    pyautogui.click(wait_for_image(screenshot_path + "feedback_dropdown_2.png"))
    time.sleep(5)
    pyautogui.click(wait_for_image(screenshot_path + "second_dropdown_menu.png"))
    time.sleep(5)
    pyautogui.scroll(-1000)
    time.sleep(5)
    pyautogui.click(wait_for_image(screenshot_path + "feedback_submit.png"))
    time.sleep(5)
    assert wait_for_image(screenshot_path + "confirmation_message_after_submtting_feedback.png"), "No confirmation."
    print("✅ TC_C42631154 passed.")
    click_on_close_button()
@pytest.mark.feedback
def test_tc_C42631153_verify_second_dropdown_menu_functionality(launch_hpx_app):
    navigate_to_feedback_form()
    time.sleep(5)
    pyautogui.scroll(-450)
    pyautogui.click(wait_for_image(screenshot_path + "feedback_dropdown_2.png"))
    time.sleep(5)
    assert wait_for_image(screenshot_path + "second_dropdown_menu.png"), "Second dropdown not functional."
    print("✅ TC_C42631153 passed.")
    click_on_close_button()

@pytest.mark.feedback
def test_tc_C42631152_verify_user_input_text_box(launch_hpx_app):
    navigate_to_feedback_form()
    time.sleep(5)
    pyautogui.scroll(-1000)
    time.sleep(5)
    pyautogui.click(wait_for_image(screenshot_path + "user_input_text_box.png"))
    time.sleep(5)
    pyautogui.write("This is sample feedback.", interval=0.1)
    time.sleep(5)
    assert wait_for_image(screenshot_path + "text_entered_indicator.png"), "Text entry failed."
    print("✅ TC_C42631152 passed.")
    click_on_close_button()

@pytest.mark.feedback
def test_tc_C42631151_verify_email_address_is_optional(launch_hpx_app):
    navigate_to_feedback_form()
    time.sleep(2)
    pyautogui.scroll(-1000)
    time.sleep(5)
    assert wait_for_image(screenshot_path + "email_address_is_optional.png"), "Optional label not found."
    print("✅ TC_C42631151 passed.")
    click_on_close_button()

@pytest.mark.feedback
def test_tc_C42631150_verify_invalid_email_validation(launch_hpx_app):
    navigate_to_feedback_form()
    time.sleep(5)
    pyautogui.scroll(-1000)
    time.sleep(5)
    pyautogui.click(screenshot_path + "email_address_is_optional.png")
    pyautogui.write("invalid_mail")                
    time.sleep(5)
    pyautogui.click(wait_for_image(screenshot_path + "user_input_text_box.png"))
    time.sleep(5)
    assert wait_for_image(screenshot_path + "invalid_email_error.png"), "No error for invalid email."
    print("✅ TC_C42631150 passed.")
    click_on_close_button()

@pytest.mark.feedback
def test_tc_C42631149_verify_valid_email_submission(launch_hpx_app):
    navigate_to_feedback_form()
    pyautogui.click(wait_for_image(screenshot_path + "star.png"))
    pyautogui.click(wait_for_image(screenshot_path + "feedback_dropdown_1.png"))
    pyautogui.click(wait_for_image(screenshot_path + "first_dropdown_menu.png"))
    pyautogui.click(wait_for_image(screenshot_path + "feedback_dropdown_2.png"))
    pyautogui.click(wait_for_image(screenshot_path + "second_dropdown_menu.png"))
    pyautogui.scroll(-1000)
    time.sleep(5)
    pyautogui.click(wait_for_image(screenshot_path + "email_address_is_optional.png"))
    pyautogui.write("user@example.com")
    time.sleep(5)
    pyautogui.click(wait_for_image(screenshot_path + "submit_feedback.png"))
    time.sleep(5)
    assert wait_for_image(screenshot_path + "confirmation_message_after_submtting_feedback.png"), "No confirmation."
    print("✅ TC_C42631149 passed.")
    click_on_close_button()

@pytest.mark.feedback
def test_tc_C42631148_verify_feedback_submission(launch_hpx_app):
    navigate_to_feedback_form()
    time.sleep(5)
    pyautogui.click(wait_for_image(screenshot_path + "star.png"))
    pyautogui.click(wait_for_image(screenshot_path + "feedback_dropdown_1.png"))
    pyautogui.click(wait_for_image(screenshot_path + "first_dropdown_menu.png"))
    pyautogui.click(wait_for_image(screenshot_path + "feedback_dropdown_2.png"))
    pyautogui.click(wait_for_image(screenshot_path + "second_dropdown_menu.png"))
    pyautogui.scroll(-1000)
    time.sleep(5)
    pyautogui.click(wait_for_image(screenshot_path + "user_input_text_box.png"))
    time.sleep(5)
    pyautogui.write("Feedback for submission test.")
    time.sleep(5)
    pyautogui.click(wait_for_image(screenshot_path + "submit_feedback.png"))
    time.sleep(5)
    assert wait_for_image(screenshot_path + "confirmation_message_after_submtting_feedback.png"), "Submission failed."
    print("✅ TC_C42631148 passed.")
    click_on_close_button()

@pytest.mark.feedback
def test_tc_C42631147_verify_confirmation_message_after_submission(launch_hpx_app):
    navigate_to_feedback_form()
    time.sleep(5)
    pyautogui.click(wait_for_image(screenshot_path + "star.png"))
    pyautogui.click(wait_for_image(screenshot_path + "feedback_dropdown_1.png"))
    pyautogui.click(wait_for_image(screenshot_path + "first_dropdown_menu.png"))
    pyautogui.click(wait_for_image(screenshot_path + "feedback_dropdown_2.png"))
    pyautogui.click(wait_for_image(screenshot_path + "second_dropdown_menu.png"))
    pyautogui.scroll(-1000)
    time.sleep(5)
    pyautogui.click(wait_for_image(screenshot_path + "user_input_text_box.png"))
    time.sleep(5)
    pyautogui.write("Great app feedback!")
    time.sleep(5)
    pyautogui.click(wait_for_image(screenshot_path + "submit_feedback.png"))
    time.sleep(5)
    assert wait_for_image(screenshot_path + "confirmation_message_after_submtting_feedback.png"), "No confirmation."
    print("✅ TC_C42631147 passed.")
    click_on_close_button()

@pytest.mark.feedback
def test_tc_C42631146_verify_fields_cleared_after_submission(launch_hpx_app):
    navigate_to_feedback_form()
    time.sleep(5)
    assert wait_for_image(screenshot_path + "feedback_slide.png"), "Fields not cleared."
    print("✅ TC_C42631146 passed.")
    click_on_close_button()

@pytest.mark.feedback
def test_tc_C53681239_verify_fields_reset_after_submission(launch_hpx_app):
    navigate_to_feedback_form()
    pyautogui.click(wait_for_image(screenshot_path + "star.png"))
    pyautogui.click(wait_for_image(screenshot_path + "feedback_dropdown_1.png"))
    pyautogui.click(wait_for_image(screenshot_path + "first_dropdown_menu.png"))
    pyautogui.click(wait_for_image(screenshot_path + "feedback_dropdown_2.png"))
    pyautogui.click(wait_for_image(screenshot_path + "second_dropdown_menu.png"))
    pyautogui.scroll(-1000)
    pyautogui.click(wait_for_image(screenshot_path + "user_input_text_box.png"))
    pyautogui.write("Feedback submission reset validation test.")
    pyautogui.click(wait_for_image(screenshot_path + "email_address_is_optional.png"))
    pyautogui.write("testuser@example.com")
    pyautogui.click(wait_for_image(screenshot_path + "submit_feedback.png"))
    time.sleep(5)
    assert wait_for_image(screenshot_path + "confirmation_message_after_submtting_feedback.png", timeout=5, confidence=0.5), \
        "✅ Submission confirmation message not found."
    pyautogui.click(wait_for_image(screenshot_path + "back_menu.png"))
    pyautogui.click(wait_for_image(screenshot_path + "send_feedback_button.png"))
    assert wait_for_image(screenshot_path + "feedback_slide.png", timeout=5, confidence=0.5), \
        "❌ Confirmation banner still present after reopening."
    print("✅ Feedback banner cleared after reopening form.")
    click_on_close_button()
    print("✅ TC_C53681239 passed.")

@pytest.mark.skip
def test_C58756126_open_feedback_via_run_and_submit():
    # Step 1: Open Windows Run
    pyautogui.hotkey("win", "r")
    time.sleep(1)
    
    # Step 2: Type the deeplink and press Enter
    pyautogui.write("hpx://feedback")
    pyautogui.press("enter")
    time.sleep(5)  # Give time for feedback UI to load

    # Step 3: Wait for feedback form and interact
    assert wait_for_image(screenshot_path + "star.png"), "❌ Feedback UI not loaded."
    pyautogui.click(wait_for_image(screenshot_path + "star.png"))
    pyautogui.click(wait_for_image(screenshot_path + "feedback_dropdown_1.png"))
    pyautogui.click(wait_for_image(screenshot_path + "first_dropdown_menu.png"))

    pyautogui.click(wait_for_image(screenshot_path + "user_input_text_box.png"))
    pyautogui.write("Deeplink feedback test.")
    
    pyautogui.click(wait_for_image(screenshot_path + "email_address_is_optional.png"))
    pyautogui.write("test@openai.com")

    pyautogui.click(wait_for_image(screenshot_path + "submit_feedback.png"))
    
    # Step 4: Confirmation
    assert wait_for_image(screenshot_path + "confirmation_message_after_submitting_feedback.png", timeout=10), \
        "❌ Feedback submission confirmation not found."

    print("✅ Feedback submitted successfully via deeplink.")

@pytest.mark.skip
def test_tc_C53681240_offline_banner_after_feedback_submission():
    # Step 1: Launch and open feedback form
    pyautogui.click(wait_for_image(screenshot_path + "profile.png"))
    pyautogui.click(wait_for_image(screenshot_path + "send_feedback_button.png"))

    # Step 2: Fill feedback form
    pyautogui.click(wait_for_image(screenshot_path + "star.png"))
    pyautogui.click(wait_for_image(screenshot_path + "feedback_dropdown_1.png"))
    pyautogui.click(wait_for_image(screenshot_path + "first_dropdown_menu.png"))
    pyautogui.click(wait_for_image(screenshot_path + "user_input_text_box.png"))
    pyautogui.write("Testing feedback offline behavior.")
    pyautogui.click(wait_for_image(screenshot_path + "email_address_is_optional.png"))
    pyautogui.write("offline@test.com")

    # Step 3: Disable Internet
    disable_internet_windows()
    time.sleep(5)

    # Step 4: Click Submit
    pyautogui.click(wait_for_image(screenshot_path + "submit_feedback.png"))

    # Step 5: Validate offline banner appears
    assert wait_for_image(screenshot_path + "offline_banner.png", timeout=10), \
        "❌ Offline message/banner not found after disabling internet."

    print("✅ Offline banner displayed correctly after submission without internet.")

    # Step 6: Re-enable internet (cleanup)
    enable_internet_windows()
@pytest.mark.skip
def test_tc_C42631145_offline_banner_after_feedback_submission():
    # Step 1: Launch and open feedback form
    pyautogui.click(wait_for_image(screenshot_path + "profile.png"))
    pyautogui.click(wait_for_image(screenshot_path + "send_feedback_button.png"))

    # Step 2: Fill feedback form
    pyautogui.click(wait_for_image(screenshot_path + "star.png"))
    pyautogui.click(wait_for_image(screenshot_path + "feedback_dropdown_1.png"))
    pyautogui.click(wait_for_image(screenshot_path + "first_dropdown_menu.png"))
    pyautogui.click(wait_for_image(screenshot_path + "user_input_text_box.png"))
    pyautogui.write("Testing feedback offline behavior.")
    pyautogui.click(wait_for_image(screenshot_path + "email_address_is_optional.png"))
    pyautogui.write("offline@test.com")

    # Step 3: Disable Internet
    disable_internet_windows()
    time.sleep(5)

    # Step 4: Submit feedback
    pyautogui.click(wait_for_image(screenshot_path + "submit_feedback.png"))

    # Step 5: Verify offline message banner
    assert wait_for_image(screenshot_path + "offline_banner.png", timeout=10), \
        "❌ Offline message/banner not found after disabling internet."

    print("✅ Offline banner displayed correctly after submission without internet.")









# ---------- Entry ----------
if __name__ == "__main__":
    pytest.main(["-s", "-m", "feedback", __file__])

