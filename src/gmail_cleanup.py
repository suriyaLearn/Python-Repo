import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class GmailCleanup:
    def __init__(self, debug_address="127.0.0.1:9222"):
        self.chrome_options = Options()
        self.chrome_options.add_experimental_option("debuggerAddress", debug_address)
        self.driver = webdriver.Chrome(options=self.chrome_options)

    def switch_to_first_tab(self):
        self.driver.switch_to.window(self.driver.window_handles[0])
        print(f"Current page title: {self.driver.title}")

    def wait_for_element(self, selector, timeout=10):
        return WebDriverWait(self.driver, timeout).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
        )

    def click_element(self, selector):
        element = self.wait_for_element(selector)
        self.driver.execute_script("arguments[0].click();", element)

    def delete_emails(self):
        while True:
            try:
                # Wait for the Delete button to be invisible (indicating no emails are selected)
                WebDriverWait(self.driver, 10).until(
                    EC.invisibility_of_element_located((By.CSS_SELECTOR, "div[data-tooltip='Delete']"))
                )

                # Click the checkbox to select all emails
                self.click_element("div[aria-label='Select']>div>span")

                # Click the Delete button
                self.click_element("div[data-tooltip='Delete']")

                time.sleep(1)  # Short pause to allow the UI to update
            except Exception as e:
                print(f"An error occurred: {e}")
                break

    def run(self):
        self.switch_to_first_tab()
        self.delete_emails()

if __name__ == "__main__":
    cleanup = GmailCleanup()
    cleanup.run()