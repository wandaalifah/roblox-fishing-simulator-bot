# Import necessary libraries
from pydoc import cli
import threading
from pyautogui import *
import pyautogui
import time
import keyboard
import random
import win32api, win32con
import pydirectinput

# Static Variables for user
bag_capacity: int = 100 # The number of fish you can hold before selling
max_wait_time: float = 10.0
x_range: list[int] = [275, 1650] # The pixel range to check for bubbles
y_range: list[int] = [120, 885] 

# Initialize counters and flags
wait_period: float = 0.025 # The time to wait between each loop
fish_counter: int = 0 # The number of fish caught
enable_fishing: bool = False # Flag to enable/disable fishing
reeling_in: bool = False # Flag to check if currently reeling in a fish
line_cast: bool = False # Flag to check if the line is cast
bubble_timer: float = 0 # Flag to check if a bubble has not popped up in a while


# Function to toggle fishing on/off
def toggle_fishing(_):
	global enable_fishing
	enable_fishing = not enable_fishing
	print(f'Fishing is now {"enabled" if enable_fishing else "disabled"}')

# Bind 'f' key to toggle fishing
keyboard.on_press_key('q', toggle_fishing)

# Function to disable the casting line after 10 seconds
def cast_disable():
	global line_cast, reeling_in
	line_cast = False
	reeling_in = False
	click_random_throw()

cast_timer = threading.Timer(max_wait_time, cast_disable)


# Function to simulate a mouse click at given coordinates
def click(x, y):
	win32api.SetCursorPos((x, y))
	time.sleep(random.uniform(0.001, 0.005))
	win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
	time.sleep(random.uniform(0.001, 0.005))
	win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)

# Function to simulate a safe mouse click using pydirectinput
def delay_click(x, y):
	pydirectinput.moveTo(x, y)
	time.sleep(random.uniform(0.3, 5))
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
	for x in range(x_range[0], x_range[1], 2):
		for y in range(y_range[0], y_range[1], 3):
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


def sell_items():
	if cast_timer.is_alive() == True:
		cast_timer.cancel()
	time.sleep(1)
	# delay_click(1210, 950) # Open inventory\
	# Click the F button to open the inventory
	pydirectinput.press('f')
	time.sleep(1)
	delay_click(1075, 350) # Click the first sell button again
	time.sleep(1)
	delay_click(1200, 430) # Click the second sell button\
	time.sleep(1)
	delay_click(1130, 430) # Click to confirm selling
	time.sleep(1)
	delay_click(1389, 374) # Click the X to close the inventory
	delay_click(1389, 374) # Click the X to close the inventory


# Main loop to check for fish and bubbles until 'q' is pressed
while True:
	# Check if fishing is enabled
	if enable_fishing == False:
		time.sleep(0.1)
		continue

	# Exit program if we are at capacity
	if fish_counter >= bag_capacity and line_cast == False and reeling_in == False:
		print('Inventory full, selling...')
		sell_items()
		fish_counter = 0
		cast_disable()

	# Check if the click bar is in a certain pixel range
	# This means we are reeling in a fish currently and need to click
	if pyautogui.pixel(925, 780)[0] == 255 :# or pyautogui.pixel(860, 800)[0] == 255
		click_random_throw()
		reeling_in = True
		line_cast = False
		pass


	# Check if we are currently reeling in a fish
	if reeling_in == True:
		# Check screen to see if fish is caught
		if pyautogui.pixel(830, 800) != (83, 250, 83):
			if fish_counter == 0: # This runs when we first start fishing
				fish_counter += 1
				continue

			reeling_in = False
			line_cast = False
			fish_counter += 1
			print(f'Fish caught: {fish_counter}')
			time.sleep(0.1)
			click_random_throw()
			pass # Start fishing again
	
		if cast_timer.is_alive() == False:
			cast_timer = threading.Timer(max_wait_time, cast_disable)
			cast_timer.start()
				
	
	else: # We are not reeling in a fish
		# Check for air bubbles on screen
		if check_air_bubbles_on_screen() == True:
			# Reel in the fish
			click_random_throw()
			reeling_in = True
			bubble_timer = 0
			pass
		else:
			# Check if we have not seen a bubble in a while
			if bubble_timer > 10:
				bubble_timer = 0
				if cast_timer.is_alive() == True:
					cast_timer.cancel()
				# print(f'No bubbles found, selling...{bubble_timer}')
				sell_items()
				fish_counter = 0
				cast_disable()
			else:
				# print(f'No bubbles found, waiting...{bubble_timer}')
				bubble_timer += wait_period

		if line_cast == False:
			line_cast = True
			# Cast the line
			click_random_throw()

		if cast_timer.is_alive() == False:
			cast_timer = threading.Timer(max_wait_time, cast_disable)
			cast_timer.start()


	time.sleep(wait_period)
