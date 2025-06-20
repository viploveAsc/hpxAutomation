# HPX Automation Framework

> 🔧 Hybrid test automation framework for the HPX (MYHP rebranding) Windows application, combining Appium, PyWinAuto, PyAutoGUI, OCR, and intelligent test design.

---

## 🚀 Overview

`hpxAutomation` is a robust test automation framework purpose-built for validating the HPX Windows desktop application. It supports visual automation, UI element interaction, OCR-based validation, and remote execution.

The framework integrates multiple tools to address real-world automation challenges across regions (US, China, Global) and application modules (accessibility, consents, onboarding, etc.).

---

## 🧰 Tech Stack

- **Test Runner**: `pytest` with `pytest-html` for reporting  
- **Windows UI Automation**: `pywinauto`, `Appium-Python-Client`  
- **Visual Control & OCR**: `pyautogui`, `pytesseract`, `Pillow`  
- **Window Management**: `pygetwindow`  
- **Remote Execution**: SSH-based trigger mechanism  
- **Intelligent Locator Strategy**: XML-based mapping system  
- **ICL Capabilities**: Uses prompts and test constraints to guide script behavior

---

## 📦 Dependencies

Install all requirements:

```bash
pip install -r requirements.txt
