# Import necessary libraries
from pyautogui import *
import pyautogui
import time
import keyboard
import random
import win32api, win32con

# Function to simulate a mouse click at given coordinates
def click(x, y):
    win32api.SetCursorPos((x, y))
    time.sleep(random.uniform(0.01, 0.05))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
    time.sleep(random.uniform(0.01, 0.05))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)

# Function to simulate a random throw click (casting the rod)
def click_random_throw():
    x, y = random.randint(960, 970), random.randint(520, 530)
    win32api.SetCursorPos((x, y))
    time.sleep(random.uniform(0.001, 0.005))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
    time.sleep(random.uniform(0.001, 0.005))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)

# Function to simulate reeling the fish with a set number of clicks
def reel_in_fish():
    for _ in range(8):  # Adjust the number of clicks for reeling
        click_random_throw()
        time.sleep(random.uniform(0.5, 0.7))  # Adjust delay between each reel click

# Function to check for air bubbles on the screen
def check_air_bubbles_on_screen():
    s = pyautogui.screenshot()
    for x in range(770, 1160):
        for y in range(350, 730):
            colorcode = (68, 252, 234)  # Blue bubbles / Blaue Blasen
            tempvar = False
            for x2 in range(5):
                if s.getpixel((x + x2, y)) == colorcode:
                    tempvar = True
                else:
                    tempvar = False
                    break
            if tempvar is True:
                return True
    return False

# Initialize counters and flags
counter = 150  # Starting counter for the rod cast timing
fish_counter = 0  # Tracks the number of fish caught
fish_found = False  # Tracks whether a fish was found

# Main loop to check for fish and bubbles until 'q' is pressed
while not keyboard.is_pressed('q'):
    # Check if fish is found
    if pyautogui.pixel(847, 820)[0] == 255 or pyautogui.pixel(860, 800)[0] == 255:
        # Fish detected, reel in
        print("Fish found! Reeling in...")
        reel_in_fish()  # Start the reeling process
        fish_found = True
        counter = 150  # Reset counter for next fish

    # Increase fish counter if found and reeling is complete
    if fish_found:
        # Check if the fish is fully reeled in (adjust the condition based on your game)
        if pyautogui.pixel(830, 800) != (83, 250, 83):  # Check when the fish is reeled in
            fish_counter += 1
            print('Fish caught: ' + str(fish_counter))
            fish_found = False  # Reset the flag for the next fish
            counter = 0  # Reset the counter to cast the rod again

    # If no fish found, check for air bubbles
    if not fish_found:
        if check_air_bubbles_on_screen():
            print("Air bubbles detected! Reeling in...")
            reel_in_fish()
            fish_found = True
            counter = 150  # Reset counter after detecting air bubbles

    # Cast the rod again when counter is 0
    if counter == 0:
        print("Casting the rod...")
        click_random_throw()  # Cast the rod
        counter = 150  # Reset the counter for the next cycle
    
    # If inventory is full, sell
    if fish_counter >= 2000:
        print('Inventory full, selling...')
        exit()

    counter -= 1  # Decrease the counter each loop iteration
    time.sleep(0.025)  # Delay to control the loop speed
