import pyautogui
import pyperclip
import requests
import time
import keyboard

# ---------------- CONFIG ----------------
OPENROUTER_API_KEY = "Bearer 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"  # <-- এখানে তোমার OpenRouter API key বসাও
MODEL = "openai/gpt-4o-mini"                          # OpenRouter model
CUSTOM_ROLE = "You are a polite Bangladeshi friend who replies shortly and friendly."
CHECK_INTERVAL = 1  # seconds
# ----------------------------------------

ENABLED = True   # F2 দিয়ে toggle হবে
last_text = ""

def ask_openrouter(prompt: str) -> str:
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": CUSTOM_ROLE},
            {"role": "user", "content": prompt},
        ]
    }
    try:
        r = requests.post(url, headers=headers, json=data, timeout=60)
        r.raise_for_status()
        return r.json()["choices"][0]["message"]["content"]
    except Exception as e:
        return f"(AI error: {e})"

def copy_selected_text():
    pyautogui.hotkey("ctrl", "c")
    time.sleep(0.2)
    return pyperclip.paste().strip()

def paste_reply(reply: str):
    pyperclip.copy(reply)
    pyautogui.hotkey("ctrl", "v")
    pyautogui.press("enter")

def toggle_enable():
    global ENABLED
    ENABLED = not ENABLED
    print(f"[F2] Auto-replier is now {'ON ✅' if ENABLED else 'OFF ⛔'}")

def main_loop():
    global last_text
    print("🚀 Insta Auto Replier started (PyAutoGUI + OpenRouter)")
    print("👉 শুধু মেসেজ সিলেক্ট করো, বাকি সব অটো হবে")
    print("F2 = Toggle On/Off | Ctrl+C in terminal to quit")

    while True:
        if ENABLED:
            copied = copy_selected_text()
            if copied and copied != last_text:
                last_text = copied
                print(f"[User] {copied}")

                reply = ask_openrouter(copied)
                print(f"[AI] {reply}")

                paste_reply(reply)
        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    keyboard.add_hotkey("F2", toggle_enable)  # Stop/On button
    try:
        main_loop()
    except KeyboardInterrupt:
        print("\nStopped by user.")
