import re
import shutil

try:
    from selenium import webdriver
    from selenium.webdriver.chrome.service import Service
    from selenium.webdriver.common.keys import Keys
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.common.by import By
    from webdriver_manager.chrome import ChromeDriverManager
    SELENIUM_AVAILABLE = True
except ImportError:
    SELENIUM_AVAILABLE = False

# ─────────────────────────────────────────────
#  LAZY DRIVER INIT
#  Only create the driver when first needed,
#  not at module import time (avoids crash on import).
# ─────────────────────────────────────────────
_driver = None

def _get_driver():
    """Lazily initialize and return a headless Chrome WebDriver."""
    global _driver
    if _driver is not None:
        return _driver

    if not SELENIUM_AVAILABLE:
        print("[SEARCH] Selenium is not installed. Google search disabled.")
        return None

    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    # Auto-detect Chrome/Chromium binary on Linux
    from NetHyTechSTT.listen import _find_chrome_binary
    binary = _find_chrome_binary()
    if binary:
        chrome_options.binary_location = binary

    # Try webdriver_manager first, then system chromedriver
    try:
        service = Service(ChromeDriverManager().install())
        _driver = webdriver.Chrome(service=service, options=chrome_options)
    except Exception:
        chromedriver_path = shutil.which("chromedriver")
        if chromedriver_path:
            try:
                service = Service(executable_path=chromedriver_path)
                _driver = webdriver.Chrome(service=service, options=chrome_options)
            except Exception as e:
                print(f"[SEARCH] Failed to init WebDriver: {e}")
                return None
        else:
            try:
                _driver = webdriver.Chrome(options=chrome_options)
            except Exception as e:
                print(f"[SEARCH] All WebDriver attempts failed: {e}")
                return None

    _driver.get("https://www.google.com")
    return _driver


def search_brain(text):
    driver = _get_driver()
    if driver is None:
        return "Search is unavailable — Chrome/Chromium not found."

    try:
        # Find the search box using its name attribute value
        search_box = driver.find_element("name", "q")

        # Clear the search box content
        search_box.clear()

        # Type the search query
        search_query = text
        search_box.send_keys(search_query)

        # Submit the form
        search_box.send_keys(Keys.RETURN)

        # Wait for a few seconds (you may need to adjust this based on your internet speed)
        driver.implicitly_wait(5)

        # Find the first search result element
        first_result = driver.find_element(By.CSS_SELECTOR, 'div.g')

        # Extract and print the first 3-4 sentences from the first search result, excluding links and dates
        first_result_text = first_result.text
        sentences = re.split(r'(?<=[.!?])\s', first_result_text)

        # Filter out sentences containing common link and date patterns
        filtered_sentences = [sentence for sentence in sentences if not re.search(r'https?://\S+|(\d{1,2} [A-Za-z]+ \d{10})', sentence)]

        # Join the remaining sentences
        result_text = '. '.join(filtered_sentences[:10])
        result_text = result_text.replace("Featured snippet from the web","")
        return result_text

    except Exception as e:
        print("An error occurred:", e)