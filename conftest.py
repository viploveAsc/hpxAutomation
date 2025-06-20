# conftest.py
import pytest
import time
import logging
import logging.config
import os
import pyautogui
import pytest
import configparser
import os

@pytest.fixture
def wait_for_image():


    def _wait(image, timeout=10, confidence=0.6):
        start_time = time.time()
        while True:
            try:
                location = pyautogui.locateCenterOnScreen(image, confidence=confidence)
                if location:
                    return location
            except Exception as e:
                print(f"Warning: {e}")
            if time.time() - start_time > timeout:
                return None
            time.sleep(1)
    return _wait


@pytest.fixture(scope="session", autouse=True)
def configure_logging():
    log_config_path = os.path.join(os.path.dirname(__file__), "logging.conf")
    logging.config.fileConfig(log_config_path, disable_existing_loggers=False)
    logging.info("Logging is configured.")


@pytest.fixture(scope="session")
def credentials():
    config = configparser.ConfigParser()
    config.read("test_data/test_config.ini")
    return {
        "username": config.get("credentials", "username"),
        "password": config.get("credentials", "password")
    }