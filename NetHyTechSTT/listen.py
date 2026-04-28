import platform
import shutil

try:
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.chrome.service import Service
    from selenium.webdriver.chrome.options import Options
    from webdriver_manager.chrome import ChromeDriverManager
    SELENIUM_AVAILABLE = True
except ImportError:
    SELENIUM_AVAILABLE = False
from os import getcwd

import os
Recog_File = os.path.join(getcwd(), "input.txt")


# ─────────────────────────────────────────────
#  CROSS-PLATFORM CHROME BINARY DETECTION
# ─────────────────────────────────────────────
def _find_chrome_binary() -> str | None:
    """
    Locate the Chrome or Chromium binary on the current OS.
    Returns the path string, or None if nothing is found.
    """
    system = platform.system().lower()

    if system == "linux":
        # Common locations on Linux (Fedora, Ubuntu, Arch, etc.)
        candidates = [
            "google-chrome",
            "google-chrome-stable",
            "chromium",
            "chromium-browser",
            "/usr/bin/google-chrome",
            "/usr/bin/google-chrome-stable",
            "/usr/bin/chromium",
            "/usr/bin/chromium-browser",
            "/snap/bin/chromium",
        ]
    elif system == "darwin":  # macOS
        candidates = [
            "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
            "/Applications/Chromium.app/Contents/MacOS/Chromium",
        ]
    else:  # Windows
        candidates = [
            "chrome.exe",
            r"C:\Program Files\Google\Chrome\Application\chrome.exe",
            r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
        ]

    for candidate in candidates:
        # shutil.which handles PATH-based names; os.path.isfile for absolutes
        found = shutil.which(candidate) if not os.path.sep in candidate else (
            candidate if os.path.isfile(candidate) else None
        )
        if found:
            print(f"[STT] Found Chrome/Chromium binary: {found}")
            return found

    return None


def _build_chrome_options() -> "Options":
    """
    Build a Chrome Options object with cross-platform flags.
    Injects the binary path if Chrome isn't on the default PATH.
    """
    chrome_options = Options()

    # ── Auto-detect and inject binary path ──
    binary = _find_chrome_binary()
    if binary:
        chrome_options.binary_location = binary
    else:
        print("[STT][WARN] Chrome/Chromium binary NOT found on this system.")
        print("[STT][WARN] Install it with:  sudo dnf install chromium   (Fedora)")
        print("[STT][WARN]                   sudo apt install chromium-browser  (Ubuntu)")

    # ── Standard flags ──
    chrome_options.add_argument("--use-fake-ui-for-media-stream")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--remote-debugging-port=9222")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-background-timer-throttling")
    chrome_options.add_argument("--disable-backgrounding-occluded-windows")
    chrome_options.add_argument("--disable-renderer-backgrounding")
    chrome_options.add_argument("--disable-web-security")
    chrome_options.add_argument("--allow-running-insecure-content")

    return chrome_options


def _create_webdriver(chrome_options: "Options") -> "webdriver.Chrome":
    """
    Try multiple strategies to get a working Chrome WebDriver:
      1. webdriver_manager (auto-downloads matching chromedriver)
      2. System-installed chromedriver (from PATH)
      3. Final attempt — let Selenium find it automatically
    """
    # ── Attempt 1: webdriver_manager ──
    try:
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        print("[STT] WebDriver initialized via webdriver_manager.")
        return driver
    except Exception as e:
        print(f"[STT] webdriver_manager failed: {e}")

    # ── Attempt 2: System-installed chromedriver ──
    chromedriver_path = shutil.which("chromedriver")
    if chromedriver_path:
        try:
            service = Service(executable_path=chromedriver_path)
            driver = webdriver.Chrome(service=service, options=chrome_options)
            print(f"[STT] WebDriver initialized via system chromedriver: {chromedriver_path}")
            return driver
        except Exception as e:
            print(f"[STT] System chromedriver failed: {e}")

    # ── Attempt 3: Let Selenium auto-detect ──
    try:
        driver = webdriver.Chrome(options=chrome_options)
        print("[STT] WebDriver initialized via Selenium auto-detect.")
        return driver
    except Exception as e:
        print(f"[STT] All WebDriver init attempts failed: {e}")
        print("[STT] ──────────────────────────────────────────────")
        print("[STT]  TROUBLESHOOTING:")
        print("[STT]    1. Install Chrome/Chromium:")
        print("[STT]         sudo dnf install chromium        (Fedora)")
        print("[STT]         sudo apt install chromium-browser (Ubuntu)")
        print("[STT]    2. Install chromedriver:")
        print("[STT]         sudo dnf install chromedriver    (Fedora)")
        print("[STT]    3. Ensure versions match:")
        print("[STT]         chromium --version")
        print("[STT]         chromedriver --version")
        print("[STT] ──────────────────────────────────────────────")
        return None


def listen():
    if not SELENIUM_AVAILABLE:
        print("[STT] Selenium is not installed. Voice input disabled.")
        print("[STT] Install with: pip install selenium webdriver-manager")
        return

    print("Support in Youtube @NetHyTech")

    chrome_options = _build_chrome_options()
    driver = _create_webdriver(chrome_options)

    if driver is None:
        print("[STT] Could not start Chrome. Voice input is DISABLED for this session.")
        print("[STT] Jarvis will continue running — use text input if available.")
        return  # Graceful degradation — don't crash the whole app

    try:
        # Creating the URL for the website
        website = "https://allorizenproject1.netlify.app/"
        # Opening the website in the Chrome browser
        driver.get(website)

        start_button = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.ID, 'startButton')))
        start_button.click()
        print("Listening...")
        output_text = ""
        is_second_click = False
        while True:
            output_element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'output')))
            current_text = output_element.text.strip()
            if "Start Listening" in start_button.text and is_second_click:
                if output_text:
                    is_second_click = False
            elif "Listening..." in start_button.text:
                is_second_click = True
            if current_text != output_text:
                output_text = current_text
                with open(Recog_File, "w") as file:
                    file.write(output_text.lower())
                    print("User:", output_text)
    except KeyboardInterrupt:
        print("[STT] Process interrupted by user.")
    except Exception as e:
        print(f"[STT] An error occurred: {e}")
    finally:
        try:
            driver.quit()
        except Exception:
            pass
