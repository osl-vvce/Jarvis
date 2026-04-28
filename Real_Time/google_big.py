from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import re
import shutil
from selenium.webdriver.support.wait import WebDriverWait

try:
    from webdriver_manager.chrome import ChromeDriverManager
except ImportError:
    ChromeDriverManager = None


def _create_headless_driver():
    """Create a headless Chrome driver using cross-platform detection."""
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    # Auto-detect Chrome/Chromium binary
    from NetHyTechSTT.listen import _find_chrome_binary
    binary = _find_chrome_binary()
    if binary:
        chrome_options.binary_location = binary

    # Try webdriver_manager first
    if ChromeDriverManager:
        try:
            service = Service(ChromeDriverManager().install())
            return webdriver.Chrome(service=service, options=chrome_options)
        except Exception:
            pass

    # Try system chromedriver
    chromedriver_path = shutil.which("chromedriver")
    if chromedriver_path:
        try:
            service = Service(executable_path=chromedriver_path)
            return webdriver.Chrome(service=service, options=chrome_options)
        except Exception:
            pass

    # Final fallback
    try:
        return webdriver.Chrome(options=chrome_options)
    except Exception as e:
        print(f"[DEEP SEARCH] All WebDriver attempts failed: {e}")
        return None


def search_and_extract(text):
    driver = _create_headless_driver()
    if driver is None:
        return "Deep search unavailable — Chrome/Chromium not found."

    try:
        # Open Google in the browser
        driver.get("https://www.google.com")
        # Find the search box using its name attribute value
        search_box = driver.find_element("name", "q")

        # Type the search query
        search_query = text
        search_box.send_keys(search_query)

        # Submit the form
        search_box.send_keys(Keys.RETURN)

        # Wait for the search box to be present (adjust the timeout as needed)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, 'q')))

        # Find the first search result element
        first_result = driver.find_element(By.CSS_SELECTOR, 'div.g')

        # Extract the link of the first result
        first_result_link = first_result.find_element(By.CSS_SELECTOR, 'a').get_attribute('href')

        # Visit the first result link
        driver.get(first_result_link)

        # Extract the webpage content
        webpage_content = driver.page_source

        # Parse the webpage content with BeautifulSoup
        soup = BeautifulSoup(webpage_content, 'html.parser')

        # Extract text from the webpage, excluding script and style tags
        webpage_text = ' '.join([p.get_text() for p in soup.find_all('p')])

        # Extract and print the first 8-9 sentences from the webpage text
        sentences = re.split(r'(?<=[.!?])\s', webpage_text)
        result_text = '. '.join(sentences[:9])
        return result_text

    except Exception as e:
        print("An error occurred:", e)
        return "I encountered an error during the search."

    finally:
        try:
            driver.quit()
        except Exception:
            pass


#########################################
try:
    from sumy.parsers.plaintext import PlaintextParser
    from sumy.nlp.tokenizers import Tokenizer
    from sumy.summarizers.lsa import LsaSummarizer
    SUMY_AVAILABLE = True
except ImportError:
    SUMY_AVAILABLE = False

def summarize_text(text, sentences_count=5):
    if not SUMY_AVAILABLE:
        # Basic fallback: return first N sentences
        sentences = re.split(r'(?<=[.!?])\s', text)
        return '. '.join(sentences[:sentences_count])
    parser = PlaintextParser.from_string(text, Tokenizer("english"))
    summarizer = LsaSummarizer()
    summary = summarizer(parser.document, sentences_count)
    return ' '.join([str(sentence) for sentence in summary])

# Example usage
def summary(text):
    text_to_summarize = text
    summary_result = summarize_text(text_to_summarize)
    return summary_result

def deep_search(text):
    x = text
    y = search_and_extract(x)
    if y:
        x = summary(y)
    return x