from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time
import os

# Set up Chrome options
chrome_options = Options()
chrome_options.add_argument("--user-data-dir=chrome-data")  # Keep user session

# Set up the WebDriver
service = Service('path/to/chromedriver')  # Update with the correct path
driver = webdriver.Chrome(service=service, options=chrome_options)

# Open WhatsApp Web
driver.get('https://web.whatsapp.com')

# Wait for the user to scan the QR code
input("Press Enter after scanning QR code")

# Define the target number
target_number = '1234567890'  # Replace with the target number

# Search for the target number
search_box = driver.find_element(By.XPATH, '//div[@contenteditable="true"][@data-tab="3"]')
search_box.click()
search_box.send_keys(target_number)
time.sleep(2)  # Wait for search results to load

# Select the chat
chat = driver.find_element(By.XPATH, f'//span[@title="{target_number}"]')
chat.click()

# Get the emoji panel and extract all emojis
driver.find_element(By.XPATH, '//button[@title="Emoji"]').click()
time.sleep(1)
emoji_elements = driver.find_elements(By.XPATH, '//div[contains(@class, "emoji")]/span')

# Prepare label file
screenshot_path = 'path/to/save/screenshots'  # Update with the correct path
if not os.path.exists(screenshot_path):
    os.makedirs(screenshot_path)
label_file = os.path.join(screenshot_path, 'labels.txt')

with open(label_file, 'w', encoding='utf-8') as f:
    # Send each emoji one by one and save its Unicode
    message_box = driver.find_element(By.XPATH, '//div[@contenteditable="true"][@data-tab="6"]')
    message_box.click()
    for emoji_element in emoji_elements:
        emoji = emoji_element.text
        if emoji:  # Ensure it's not an empty string
            message_box.send_keys(emoji)
            message_box.send_keys(Keys.ENTER)
            time.sleep(0.5)  # Adjust delay to prevent overload
            f.write(f'{emoji} : {ord(emoji)}\n')

# Take a screenshot of the chat
screenshot_file = os.path.join(screenshot_path, 'screenshot.png')
driver.save_screenshot(screenshot_file)

# Close the WebDriver
driver.quit()