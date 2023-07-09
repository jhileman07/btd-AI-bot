import pyautogui
import time
# Size of screen: 1440x900
time.sleep(5)
pyautogui.click(908,864)
pyautogui.typewrite("Hello World (sent with AI)")
pyautogui.press("enter")
# Text Isabel a message that says "I am a bot"
pyautogui.typewrite("I am a bot")
pyautogui.press("enter")
# Open VS Code
pyautogui.click(1000,865)
# Take a screenshot of this code and send it to Isabel
pyautogui.hotkey("command", "shift", "4")
pyautogui.moveTo(445,104)
pyautogui.dragTo(1380,667,duration=1.5, button="left")
# Open Slack
pyautogui.click(908,864)
pyautogui.moveTo(1390,857)
pyautogui.dragTo(1000,785,duration=1.5, button="left")
pyautogui.typewrite("I just sent you a screenshot with AI")
pyautogui.press("enter")
pyautogui.typewrite("I am so cool bro")
pyautogui.press("enter")
# Return to VS Code
pyautogui.click(1000,865)