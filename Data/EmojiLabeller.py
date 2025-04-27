import pyautogui
import time
import os
import pyperclip

time.sleep(10)
txt_file_path = r"D:\SE\Data\emojis_unicode.txt"
with open(txt_file_path, "r", encoding="utf-8") as file:
    emoji_unicode_mapping = [line.strip().split(": ") for line in file]
        
for i in range(9, 100):
    print(i, end=", ")
    
    screenshot_path = os.path.join(r"D:\SE\Data", f"screenshots{i}")
    label_file = os.path.join(screenshot_path, 'labels.txt')
    
    os.makedirs(screenshot_path, exist_ok=True)

    with open(label_file, 'w', encoding='utf-8') as f:
        for idx, (emoji, unicode_value) in enumerate(emoji_unicode_mapping, start=1):
            pyperclip.copy(emoji)
            time.sleep(0.05)

            pyautogui.hotkey("ctrl", "v")

            pyautogui.press("enter")
            time.sleep(0.125)

            screenshot_file = os.path.join(screenshot_path, f'screenshot_{idx}.png')
            pyautogui.screenshot(screenshot_file)

            f.write(f'{os.path.basename(screenshot_file)}, {emoji}, {unicode_value}\n')
    print(i)

print("✅ All emojis sent, labeled, and screenshots saved successfully!")
