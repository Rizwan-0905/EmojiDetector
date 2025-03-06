import pyautogui
import time
import os
import pyperclip  # For clipboard handling

# Define the target contact name (as saved in WhatsApp)
target_contact = "Rizwan-2"  # Change this to the contact name

# Define the path to save screenshots
screenshot_path = 'C:/users/lms/desktop/codespace/uni/EmojiDetector/ExtraScripts/newData'
if not os.path.exists(screenshot_path):
    os.makedirs(screenshot_path)

label_file = os.path.join(screenshot_path, 'labels.txt')

# Load emojis and their Unicode hex values
emojis = ["😊", "😂", "❤️", "👍", "😭", "🔥", "😎", "🤔", "🥳", "💡"]
emoji_hex = ["U+1F60A", "U+1F602", "U+2764", "U+1F44D", "U+1F62D",
             "U+1F525", "U+1F60E", "U+1F914", "U+1F973", "U+1F4A1"]

# Open WhatsApp Desktop App
os.system("start WhatsApp")  # Works on Windows
time.sleep(7)  # Wait for WhatsApp to open

# Open search bar & find the contact
pyautogui.hotkey("ctrl", "f")  # Open search in WhatsApp Desktop
time.sleep(1)
pyautogui.write(target_contact)  # Type contact name
time.sleep(2)
pyautogui.press("enter")  # Select the chat
time.sleep(3)  # Ensure chat is open

# Open file for writing labels
with open(label_file, 'w', encoding='utf-8') as f:
    for idx, (emoji, unicode_hex) in enumerate(zip(emojis, emoji_hex), start=1):
        # Copy emoji to clipboard
        pyperclip.copy(emoji)
        time.sleep(1)

        # Paste emoji in chat
        pyautogui.hotkey("ctrl", "v")
        time.sleep(1)

        # Press enter to send
        pyautogui.press("enter")
        time.sleep(2)  # Wait for the message to send

        # Take screenshot
        screenshot_file = os.path.join(screenshot_path, f'screenshot_{idx}.png')
        pyautogui.screenshot(screenshot_file)

        # Save label as "screenshot_name, emoji, unicode"
        f.write(f'{os.path.basename(screenshot_file)}, {emoji}, {unicode_hex}\n')

print("All emojis sent, labeled, and screenshots saved successfully!")
