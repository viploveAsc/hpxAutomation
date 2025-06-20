import logging
import subprocess
import time

import pytest
import pywinauto
from pywinauto import Application

logger = logging.getLogger(__name__)


@pytest.fixture(scope="module")
def launch_hpx_app():
    logger.info("Launching the myHP app")

    # Launch UWP app via AppUserModelID
    app_id = "AD2F1837.myHP_v10z8vjag6ke6!App"
    subprocess.Popen(f"explorer shell:AppsFolder\\{app_id}", shell=True)

    time.sleep(20)  # Give it time to launch fully

    # Attach using pywinauto
    try:
        # Use backend="uia" for modern apps (UWP, Electron, etc.)
        app = Application(backend="uia")
        app.connect(title_re=".*myHP.*")  # Adjust the title pattern as needed
        main_win = app.top_window()
        logger.info("Connected to myHP main window")
        yield main_win

    except pywinauto.findwindows.ElementNotFoundError as e:
        logger.error(f"Could not connect to the myHP app: {e}")
        yield None


def test_click_notifications_and_close(launch_hpx_app):
    app_window = launch_hpx_app
    assert app_window is not None, "App window not available"

    try:
        # Step 1: Click the Notifications button
        notif_button = app_window.child_window(
            title="Notifications", control_type="Button"
        )
        notif_button.wait("enabled", timeout=10)
        notif_button.click_input()
        print("Clicked on Notifications button.")
        time.sleep(2)  # Give time for flyout to open

        # Step 2: Search for the Close button in all app windows
        from pywinauto.findwindows import find_elements

        all_controls = find_elements(title="Close", control_type="Button")
        close_btn_elem = next(
            (
                el
                for el in all_controls
                if el.automation_id == "SideFlyout.SideFlyoutView.CloseButton"
            ),
            None,
        )

        assert close_btn_elem is not None, "Close button not found"

        # Attach to the parent of the found control
        close_win = app_window.app.window(handle=close_btn_elem.handle)
        close_button = close_win.child_window(
            auto_id="SideFlyout.SideFlyoutView.CloseButton", control_type="Button"
        )
        close_button.wait("enabled", timeout=10)
        close_button.click_input()
        print("Clicked on Close button in flyout.")

    except Exception as e:
        pytest.fail(f"Failed during Notifications -> Close flow: {e}")


if __name__ == "__main__":
    pytest.main([__file__])
