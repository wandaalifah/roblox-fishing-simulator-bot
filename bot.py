# Import necessary libraries
from pydoc import cli
from pyautogui import *
import pyautogui
import time
import keyboard
import random
import win32api, win32con
import pydirectinput

# Static Variables for user
bag_capacity: int = 270
max_wait_time: float = 10.0

# Initialize counters and flags
fish_counter: int = 0 # The number of fish caught
enable_fishing: bool = False # Flag to enable/disable fishing
reeling_in: bool = False # Flag to check if currently reeling in a fish
line_cast: bool = False # Flag to check if the line is cast


# Function to toggle fishing on/off
def toggle_fishing(_):
	global enable_fishing
	enable_fishing = not enable_fishing
	print(f'Fishing is now {"enabled" if enable_fishing else "disabled"}')

# Bind 'f' key to toggle fishing
keyboard.on_press_key('q', toggle_fishing)

# Function to disable the casting line after 10 seconds
def cast_disable():
	if check_air_bubbles_on_screen() == False and reeling_in == False:
		global line_cast
		line_cast = False

# Function to simulate a mouse click at given coordinates
def click(x, y):
	win32api.SetCursorPos((x, y))
	time.sleep(random.uniform(0.001, 0.005))
	win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
	time.sleep(random.uniform(0.001, 0.005))
	win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)


# Function to simulate a safe mouse click using pydirectinput
def safety_click(x, y):
	pydirectinput.moveTo(x, y)
	time.sleep(random.uniform(0.01, 0.05))
	pydirectinput.click()


# Function to simulate a double mouse click at given coordinates
def double_click(x, y):
	click(x, y)
	time.sleep(random.uniform(0.02, 0.025))
	click(x, y)


"""
	Function to check for air bubbles on the screen
"""
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


"""
	Function to simulate a random throw click
"""
def click_random_throw():
	x, y = random.randint(960, 970), random.randint(520, 530)
	win32api.SetCursorPos((x, y))
	time.sleep(random.uniform(0.001, 0.005))
	win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
	time.sleep(random.uniform(0.001, 0.005))
	win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)


# Function to simulate a double random throw click
def double_click_random_throw():
	click_random_throw()
	time.sleep(random.uniform(0.02, 0.025))
	click_random_throw()


# Main loop to check for fish and bubbles until 'q' is pressed
while True:
	# Check if fishing is enabled
	if enable_fishing == False:
		time.sleep(0.1)
		continue

	# Check if the click bar is in a certain pixel range
	# This means we are reeling in a fish currently and need to click
	if pyautogui.pixel(925, 780)[0] == 255 :# or pyautogui.pixel(860, 800)[0] == 255
		double_click_random_throw()
		reeling_in = True
		pass

	# Check if we are currently reeling in a fish
	if reeling_in == True:
		# Check screen to see if fish is caught
		if pyautogui.pixel(830, 800) != (83, 250, 83):
			reeling_in = False
			line_cast = False
			print(f'Fish caught: {fish_counter}')
			fish_counter += 1
			time.sleep(0.1)
			click_random_throw()
			pass # Start fishing again
	
	else: # We are not reeling in a fish
		# Check for air bubbles on screen
		if line_cast == True:
			if check_air_bubbles_on_screen() == True:
				# Reel in the fish
				click_random_throw()
				reeling_in = True
				pass
		else:
			line_cast = True
			# Cast the line
			click_random_throw()
			# Wait maximum of 10 seconds for the fish to bite in a new thread and set line_cast to False
			# threading.Timer(max_wait_time, cast_disable).start()

	# Exit program if we are at capacity
	if fish_counter >= bag_capacity:
		print('Inventory full, selling...')
		break

	time.sleep(0.025)
