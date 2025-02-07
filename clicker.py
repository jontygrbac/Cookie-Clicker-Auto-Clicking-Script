from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import pyautogui
import time
import keyboard

# Set up the browser
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.get("https://orteil.dashnet.org/cookieclicker/")

# Wait for the big cookie element to load
driver.implicitly_wait(10)  # Wait up to 10 seconds

browser_offset_x = driver.get_window_position()['x']
browser_offset_y = driver.get_window_position()['y'] + driver.execute_script('return window.outerHeight - window.innerHeight;')

def center_of_element(rect):
    return rect['x'] + rect['width'] // 2, rect['y'] + rect['height'] // 2

def element_positioning(element):
    element_retrieved = driver.find_element(By.ID, element)
    position = element_retrieved.rect
    x, y = center_of_element(position)
    x += browser_offset_x
    y += browser_offset_y
    return (x, y)

#Finding the english language element
try:
    language_x, language_y = element_positioning("langSelect-EN")
    pyautogui.moveTo(language_x, language_y)
    pyautogui.click()
except Exception as e:
    print(f"Failed to find elements: {e}")
    driver.quit()
    exit()

#Finding the cookie to be clicked
try:
    cookie_x, cookie_y = element_positioning("bigCookie")
    #Alternate between products for purchase, 
    #Need to automate this so when the score reaches a certain level, it will search available products
    #e.g id=product0Price
    #cookies amount    id=cookies
    #Purchasing products that fit the budget
    product0_x, product0_y = element_positioning("product0")
    product1_x, product1_y = element_positioning("product1")
    while(keyboard.is_pressed('esc') != True):
        pyautogui.click(cookie_x, cookie_y, clicks=50, interval=0.001)
        pyautogui.click(product0_x, product0_y, clicks=1, interval=0.001)
        pyautogui.click(product1_x, product1_y, clicks=1, interval=0.001)
except Exception as e:
    print(f"Failed to find elements: {e}")
    driver.quit()
    exit()




# Clean up
time.sleep(2)
driver.quit()