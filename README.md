## Cookie Clicker Auto-Clicking Script

### Overview

This script automates interactions with the web game Cookie Clicker by leveraging the following:

- Selenium WebDriver to control the browser and locate game elements.
- PyAutoGUI to simulate mouse clicks for high-speed automation.

### Dependencies

To run the script, you need to install the following Python libraries:

```bash
pip install selenium webdriver-manager pyautogui
```

### Libraries Used

- `selenium`: Automates the browser to interact with elements on the page.
- `webdriver_manager`: Simplifies ChromeDriver management for Selenium.
- `pyautogui`: Simulates mouse movement and clicks.
- `time`: Adds delays between operations.
- `keyboard`: Allows for exit from program

### How It Works

1. Browser Setup: The script opens the Cookie Clicker website using Selenium.

2. Element Detection: It waits for the language selection button (langSelect-EN) and the bigCookie element.

3. Coordinate Calculation: Coordinates of the elements are adjusted using browser offsets for compatibility with pyautogui.

4. Mouse Actions: After calculations of element positions, the mouse will commence clicking and playing the game

## TO DO

- Clicker should also be able to purchase items from the store to increase production, this would be based on how many cookie were available to spend.
