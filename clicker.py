from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import pyautogui
import keyboard
from bs4 import BeautifulSoup

#setup variables, product lists and defaults
products = []
productsPrice = []
upgrades = []
for x in range(20):
    products.append(f"product{x}")
    productsPrice.append(f"productPrice{x}")

for x in range(716):
    upgrades.append(f'upgrade{x}')
defaultClickCount = 50


# Set up the browser
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.get("https://orteil.dashnet.org/cookieclicker/")

# Wait for the elements to load
driver.implicitly_wait(10)  # Wait up to 10 seconds
# Execute the JavaScript to get the tooltip HTML

# Offsets will be used so the clicker is always in the correct position no matter the device
browser_offset_x = driver.get_window_position()['x']
browser_offset_y = driver.get_window_position()['y'] + driver.execute_script('return window.outerHeight - window.innerHeight;')

def center_of_element(rect):
    return rect['x'] + rect['width'] // 2, rect['y'] + rect['height'] // 2

# Retrieve the element positioning, we will use this for our clicker
def element_positioning(element):
    element_retrieved = driver.find_element(By.ID, element)
    position = element_retrieved.rect
    x, y = center_of_element(position)
    x += browser_offset_x
    y += browser_offset_y
    return (x, y)

def getCookies():
    cookies = driver.find_element(By.ID, "cookies")
    return replaceToInt(cookies.text.split(" ")[0].replace(",", ""))

# Find the prices for all 20 products, if they are locked set to inf
def getPrice(product):
    price = driver.find_element(By.ID, product)
    if price.text == "":
        return float('inf')
    return replaceToInt(price.text.replace(",", ""))

def getProductPrices():
    prices = {}
    for x in productsPrice:
        prices[x] = (getPrice(x))
    return prices

def replaceToInt(value):
    # Define suffixes and their corresponding multiplier values
    suffixes = {
        "million": 10**6,
        "billion": 10**9,
        "trillion": 10**12,
        "quadrillion": 10**15,
        "quintillion": 10**18,
        "sextillion": 10**21,
        "septillion": 10**24,
        "octillion": 10**27,
        "nonillion": 10**30,
        "undecillion": 10**36,
        "duodecillion": 10**39,
        "tredecillion": 10**42,
        "quattuordecillion": 10**45,
        "quindecillion": 10**48,
        "sexdecillion": 10**51,
        "septendecillion": 10**54,
        "octodecillion": 10**57,
        "novemdecillion": 10**60,
        "vigintillion": 10**63,
        "decillion": 10**33,
        "googol": 10**100
    }

    # Clean the value by removing spaces and periods
    value = value.replace(" ", "").replace(".", "")

    # Check for suffix and multiply accordingly
    for suffix, multiplier in suffixes.items():
        if suffix in value:
            numeric_part = value.replace(suffix, "")
            return int(numeric_part) * multiplier

    # Default conversion if no suffix is found
    return int(value)

def getUpgradePrice(id):
    # Execute the JavaScript to get the tooltip HTML
    tooltip_html = driver.execute_script(f"return Game.crateTooltip(Game.UpgradesById[{id}], 'store');")

    # Parse the HTML using BeautifulSoup
    soup = BeautifulSoup(tooltip_html, 'html.parser')

    # Extract the price value
    price_element = soup.find('span', class_='price')
    if price_element:
        price_text = price_element.text.strip().replace(",", "")
        price_text = replaceToInt(price_text)
        if price_text % 10 != 0:
            price_text = float('inf')
        return price_text
    else:
        return float('inf')


def getUpgradePrices():
    upgradePrices = {}
    count = 0
    for x in upgrades:
        upgradePrices[x] = (getUpgradePrice(count))
        count += 1
    return upgradePrices 
    

# Find the lowest price and purchase it if cookies are available
def purchase(cookies, prices, clickCount):
    lowestPrice = min(prices, key=prices.get)
    lowestUpgrade = min(upgradePrices, key=upgradePrices.get)

    if upgradePrices[lowestUpgrade] < prices[lowestPrice]:
        if cookies > upgradePrices[lowestUpgrade]:
            try:
                #pyautogui.click(element_positioning(lowestUpgrade), interval=0.001)
                click_script = f"document.getElementById('{lowestUpgrade}').click();"
                driver.execute_script(click_script)
                upgradePrices.pop(lowestUpgrade)
            except:
                upgradePrices.pop(lowestUpgrade)
    elif cookies > prices[lowestPrice]:
        attemptAmounts = int(cookies / prices[lowestPrice])
        for x in range(attemptAmounts):
        #pyautogui.click(element_positioning(lowestPrice), interval=0.001)
            click_script = f"document.getElementById('{lowestPrice}').click();"
            driver.execute_script(click_script)

    clickCount = prices[lowestPrice]
    prices = getProductPrices()
    return clickCount, prices

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
    prices = getProductPrices()
    upgradePrices = getUpgradePrices()
    clickCount = defaultClickCount


# Program loop, escape will allow exit
    while(keyboard.is_pressed('esc') != True):

        pyautogui.click(cookie_x, cookie_y, clicks=clickCount, interval=0.00001)
        cookies = getCookies()
        if keyboard.is_pressed('q'):
            input("Press enter to unpause")
        
        # Proceed to purchase and return new prices and clickCounts
        clickCount, prices = purchase(cookies, prices, clickCount)

except Exception as e:
    print(f"Failed to find elements: {e}")
    driver.quit()
    exit()

driver.quit()