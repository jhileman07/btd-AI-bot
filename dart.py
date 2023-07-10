import pyautogui
import time
from random import randint, choice
import numpy as np
from PIL import Image
from scipy.stats import mode
import matplotlib.pyplot as plt

# Load image
image_path = "roadmap.png"
image = Image.open(image_path)

# Convert image to grayscale
image_gray = image.convert('L')

# Convert grayscale image to numpy array
image_gray_np = np.array(image_gray)

# Set a threshold for distinguishing between the road and non-road areas
threshold = np.mean(image_gray_np)

# Create a binary mask where the grayscale intensity is less than the threshold
not_road_mask = image_gray_np < threshold

# Get the coordinates of the non-road areas
non_road_coords = np.argwhere(not_road_mask)

# Convert the coordinates to the original image size
original_size = np.array([1440, 900])
current_size = np.array(image.size)
scale_factor = original_size / current_size

scaled_non_road_coords = non_road_coords * scale_factor

# Round the coordinates to integers
scaled_non_road_coords = np.round(scaled_non_road_coords).astype(int)

# Clip the coordinates to the original image size
scaled_non_road_coords = np.clip(scaled_non_road_coords, 0, original_size-1)

# Convert numpy array to list of tuples
non_road_pixels = [tuple(coord) for coord in scaled_non_road_coords if 0 <= coord[0] <= 1200 and 100 <= coord[1] <= 800] 


# Size of screen: 1440x900
time.sleep(5)
locTower = {
    "dart": "q",
    "boomerang" : "w",
    "bomb" : "e",
    "tack" : "r",
    "ice" : "t",
    "glue" : "y",
    "sniper" : "z",
    "sub" : "x",
    "boat" : "c",
    "ace" : "v",
    "heli" : "b",
    "mortar" : "n",
    "dartling" : "m",
    "wizard" : "a",
    "super" : "s",
    "ninja" : "d",
    "alchemist" : "f",
    "druid" : "g",
    "spike" : "j",
    "village" : "k",
    "engineer" : "l",
}

locUpgrade = {
    "path1" : ",",
    "path2" : ".",
    "path3" : "/",
}

pyautogui.typewrite("d")
pyautogui.moveTo(500,318, duration=0.5)
pyautogui.click()
pyautogui.moveTo(1390,807, duration=0.5)
pyautogui.click()
pyautogui.click()
placedTowers = []
while True:
    if currMoney > 250:
      rand = randint(0,10)
      if rand > 8:
          pyautogui.typewrite(choice(list(locTower.keys())))
          coords = choice(non_road_pixels)
          x = coords[0]
          y = coords[1]
          pyautogui.moveTo(x,y, duration=0.5)
          pyautogui.click()
          placedTowers.append([x,y])
      elif placedTowers:
          coords = choice(placedTowers)
          pyautogui.moveTo(coords[0],coords[1], duration=0.5)
          pyautogui.click()
          pyautogui.typewrite(choice(list(locUpgrade.keys())))