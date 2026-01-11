#!/usr/bin/env python3
"""
Edu Mail Generator - Modernized Version
Generates educational email accounts automatically
"""

import time
import re
import string
import random
import sys
import os
import logging
from typing import Optional, Tuple, Dict, Any
import colorama
from seleniumwire import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
import seleniumwire.undetected_chromedriver.v2 as uc
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager

try:
    from config import Config
    from __constants.const import *
    from __banner.myBanner import bannerTop
    from __colors__.colors import *
    from helper import EduHelper
except ImportError as e:
    print(f"Import error: {e}")
    print("Please run setup_modern.py first or ensure all files are present")
    sys.exit(1)

# Initialize colorama for Windows compatibility
colorama.init()

class EduMailGenerator:
    """Main class for generating educational email accounts"""
    
    def __init__(self):
        self.config = Config()
        self.setup_logging()
        self.driver = None
        
    def setup_logging(self):
        """Setup logging configuration"""
        log_level = getattr(logging, self.config.get('log_level', 'INFO'))
        logging.basicConfig(
            level=log_level,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('edu_generator.log'),
                logging.StreamHandler(sys.stdout)
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def setup_webdriver(self) -> webdriver:
        """Setup and return webdriver instance"""
        browser = self.config.get_browser_preference()
        
        try:
            if browser == 'chrome':
                options = ChromeOptions()
                if self.config.get('headless'):
                    options.add_argument('--headless')
                options.add_argument('--no-sandbox')
                options.add_argument('--disable-dev-shm-usage')
                options.add_argument('--disable-blink-features=AutomationControlled')
                options.add_experimental_option("excludeSwitches", ["enable-automation"])
                options.add_experimental_option('useAutomationExtension', False)
                
                service = Service(ChromeDriverManager().install())
                driver = webdriver.Chrome(service=service, options=options)
                
            elif browser == 'firefox':
                options = FirefoxOptions()
                if self.config.get('headless'):
                    options.add_argument('--headless')
                
                service = FirefoxService(GeckoDriverManager().install())
                driver = webdriver.Firefox(service=service, options=options)
                
            elif browser == 'chrome_undetected':
                options = uc.ChromeOptions()
                if self.config.get('headless'):
                    options.add_argument('--headless')
                driver = uc.Chrome(options=options)
                
            else:
                raise ValueError(f"Unsupported browser: {browser}")
            
            # Set implicit wait
            driver.implicitly_wait(10)
            return driver
            
        except Exception as e:
            self.logger.error(f"Failed to setup webdriver: {e}")
            raise
    
    def generate_random_phone(self) -> str:
        """Generate a random phone number"""
        first = str(random.choice(country_codes))
        second = str(random.randint(100, 999))
        last = str(random.randint(1000, 9999))
        while last in ['1111', '2222', '3333', '4444', '5555', '6666', '7777', '8888']:
            last = str(random.randint(1000, 9999))
        return f'{first}-{second}-{last}'
    
    def wait_for_element(self, by: By, value: str, timeout: int = None) -> Optional[Any]:
        """Wait for element with timeout"""
        if timeout is None:
            timeout = self.config.get('timeout', 60)
        
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((by, value))
            )
            return element
        except Exception as e:
            self.logger.error(f"Element not found: {by}={value}, Error: {e}")
            return None
    
    def safe_click(self, by: By, value: str, timeout: int = None) -> bool:
        """Safely click an element"""
        try:
            element = self.wait_for_element(by, value, timeout)
            if element:
                element.click()
                time.sleep(self.config.get('delay_between_actions', 0.7))
                return True
        except Exception as e:
            self.logger.error(f"Failed to click element: {by}={value}, Error: {e}")
        return False
    
    def safe_send_keys(self, by: By, value: str, text: str, timeout: int = None) -> bool:
        """Safely send keys to an element"""
        try:
            element = self.wait_for_element(by, value, timeout)
            if element:
                element.clear()
                element.send_keys(text)
                time.sleep(self.config.get('delay_between_actions', 0.7))
                return True
        except Exception as e:
            self.logger.error(f"Failed to send keys to element: {by}={value}, Error: {e}")
        return False
    
    def select_dropdown_option(self, by: By, value: str, option_value: str) -> bool:
        """Select option from dropdown"""
        try:
            element = self.wait_for_element(by, value)
            if element:
                select = Select(element)
                select.select_by_value(option_value)
                time.sleep(self.config.get('delay_between_actions', 0.7))
                return True
        except Exception as e:
            self.logger.error(f"Failed to select dropdown option: {by}={value}, Error: {e}")
        return False
    
    def display_banner(self):
        """Display application banner"""
        try:
            print(bannerTop())
        except:
            print("=== EDU MAIL GENERATOR ===")
            print("Modernized Version with GitHub Secrets Support")
            print("=" * 50)
    
    def select_college(self) -> Tuple[str, int]:
        """Let user select a college"""
        # Check for environment variable first (for CI/non-interactive mode)
        college_id_env = os.environ.get('COLLEGE_ID')
        if college_id_env:
            try:
                college_id = int(college_id_env)
                if 1 <= college_id <= len(allColleges):
                    selected_college = allColleges[college_id - 1]
                    self.logger.info(f"Using college ID from environment: {college_id} - {selected_college}")
                    print(f"\n{fc}{sd}[{fm}{sb}*{fc}{sd}] {fg}Selected (from env): {fy}{selected_college}")
                    return selected_college, college_id - 1
                else:
                    self.logger.warning(f"Invalid COLLEGE_ID from environment: {college_id_env}. Must be 1-{len(allColleges)}")
            except ValueError:
                self.logger.warning(f"Invalid COLLEGE_ID format from environment: {college_id_env}")
        
        # Fall back to interactive mode
        print(f"{fc}{sd}[{fm}{sb}*{fc}{sd}] {fg}Select a college from available options:\n")
        
        # Display colleges with colors
        bad_colors = ['BLACK', 'WHITE', 'LIGHTBLACK_EX', 'RESET']
        codes = vars(colorama.Fore)
        colors = [codes[color] for color in codes if color not in bad_colors]
        
        for index, college in enumerate(allColleges):
            color = random.choice(colors)
            print(f"{fc}{sd}[{fm}{sb}*{fc}{sd}] {fy}{index + 1} - {color}{college}")
        
        while True:
            try:
                choice = input(f"\n{fc}{sd}[{fm}{sb}*{fc}{sd}] {fg}Enter college ID (1-{len(allColleges)}): ")
                college_id = int(choice)
                if 1 <= college_id <= len(allColleges):
                    selected_college = allColleges[college_id - 1]
                    print(f"\n{fc}{sd}[{fm}{sb}*{fc}{sd}] {fg}Selected: {fy}{selected_college}")
                    return selected_college, college_id - 1
                else:
                    print(f"{fc}{sd}[{fm}{sb}*{fc}{sd}] {fr}Invalid ID. Please enter 1-{len(allColleges)}")
            except ValueError:
                print(f"{fc}{sd}[{fm}{sb}*{fc}{sd}] {fr}Please enter a valid number")
    
    def get_user_email(self) -> str:
        """Get user email from environment or input"""
        email = self.config.get_email_from_env()
        if email:
            print(f"{fc}{sd}[{fm}{sb}*{fc}{sd}] {fg}Using email: {fy}{email}")
        return email
    
    def start_registration(self, start_url: str, email: str, college: str, college_id: int, cookies: dict, token: str) -> bool:
        """Start the registration process"""
        try:
            # Setup interceptor
            def interceptor(request):
                if request.method == 'POST' and 'Cumberland' in request.url:
                    request.abort(403)

            self.driver.request_interceptor = interceptor

            # Inject cookies
            print(f"{fc}{sd}[{fm}{sb}*{fc}{sd}] {fg}Injecting Incap cookies...")
            cookies['reese84'] = token

            self.driver.get('https://www.openccc.net')
            for cookie_name, cookie_value in cookies.items():
                cookie_dict = {'name': cookie_name, 'value': cookie_value, 'domain': '.openccc.net'}
                self.driver.add_cookie(cookie_dict)

            print(f"{fc}{sd}[{fm}{sb}*{fc}{sd}] {fg}Incapsula bypass successful")

            # Navigate to registration page
            self.driver.get(start_url)
            self.driver.maximize_window()

            # Generate random data
            student_phone = self.generate_random_phone()
            middle_name = random.choice(string.ascii_uppercase)

            # Parse address
            address_parts = studentAddress.split("\n")
            street_address = address_parts[0]

            if ',' in address_parts[1]:
                city_state = address_parts[1].split(', ')
                city = city_state[0]
                state_zip = city_state[1].split(' ')
                state = state_zip[0]
                postal_code = state_zip[1] if len(state_zip) > 1 else '90210'
            else:
                parts = address_parts[1].split(' ')
                city = parts[0] if len(parts) > 0 else 'Los Angeles'
                state = parts[1] if len(parts) > 1 else 'CA'
                postal_code = parts[2] if len(parts) > 2 else '90210'

            # Start filling the form
            return self.fill_registration_form(email, student_phone, middle_name, street_address, city, state, postal_code, college_id)

        except Exception as e:
            self.logger.error(f"Registration failed: {e}")
            return False

    def run(self):
        """Main execution method"""
        try:
            self.display_banner()

            # Get user inputs
            college_name, college_index = self.select_college()
            user_email = self.get_user_email()

            # Setup webdriver
            print(f"{fc}{sd}[{fm}{sb}*{fc}{sd}] {fg}Setting up browser...")
            self.driver = self.setup_webdriver()

            # Perform Incapsula bypass
            print(f"{fc}{sd}[{fm}{sb}*{fc}{sd}] {fg}Performing Incapsula bypass...")
            helper = EduHelper(clg_ids[college_index])
            start_url, cookies, token = helper._tryHarder()

            # Start the registration process
            print(f"{fc}{sd}[{fm}{sb}*{fc}{sd}] {fg}Starting registration process...")
            success = self.start_registration(start_url, user_email, college_name, college_index + 1, cookies, token)

            if success:
                print(f"{fc}{sd}[{fm}{sb}*{fc}{sd}] {fg}Registration completed successfully!")
            else:
                print(f"{fc}{sd}[{fm}{sb}*{fc}{sd}] {fr}Registration failed!")

        except KeyboardInterrupt:
            print(f"\n{fc}{sd}[{fm}{sb}*{fc}{sd}] {fy}Process interrupted by user")
        except Exception as e:
            self.logger.error(f"Unexpected error: {e}")
            print(f"{fc}{sd}[{fm}{sb}*{fc}{sd}] {fr}Unexpected error: {e}")
        finally:
            if self.driver:
                self.driver.quit()
                print(f"{fc}{sd}[{fm}{sb}*{fc}{sd}] {fg}Browser closed")

    def fill_registration_form(self, email: str, phone: str, middle_name: str,
                             street: str, city: str, state: str, postal: str, college_id: int) -> bool:
        """Fill the registration form"""
        try:
            # Wait for form to load
            time.sleep(5)

            # Check if we need to click a button first
            try:
                submit_btn = self.wait_for_element(By.ID, "accountFormSubmit", 10)
                if submit_btn and submit_btn.is_displayed():
                    submit_btn.click()
                    time.sleep(5)
            except:
                pass

            # Fill personal information
            print(f"{fc}{sd}[{fm}{sb}*{fc}{sd}] {fy}Account Progress - 1/3", end='')

            if not self.safe_send_keys(By.ID, "inputFirstName", firstName):
                return False
            if not self.safe_send_keys(By.ID, "inputMiddleName", middle_name):
                return False
            if not self.safe_send_keys(By.ID, "inputLastName", LastName):
                return False

            # Click radio buttons
            if not self.safe_click(By.XPATH, '//*[@id="hasOtherNameNo"]'):
                return False
            if not self.safe_click(By.XPATH, '//*[@id="hasPreferredNameNo"]'):
                return False

            # Fill birth date
            if not self.select_dropdown_option(By.ID, 'inputBirthDateMonth', str(randomMonth)):
                return False
            if not self.select_dropdown_option(By.ID, 'inputBirthDateDay', str(randomDay)):
                return False
            if not self.safe_send_keys(By.ID, 'inputBirthDateYear', str(randomYear)):
                return False

            # Confirm birth date
            if not self.select_dropdown_option(By.ID, 'inputBirthDateMonthConfirm', str(randomMonth)):
                return False
            if not self.select_dropdown_option(By.ID, 'inputBirthDateDayConfirm', str(randomDay)):
                return False
            if not self.safe_send_keys(By.ID, 'inputBirthDateYearConfirm', str(randomYear)):
                return False

            # SSN option
            if not self.safe_click(By.ID, '-have-ssn-no'):
                return False

            time.sleep(2)

            # Submit first page
            element = self.wait_for_element(By.ID, 'accountFormSubmit')
            if element:
                self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
                time.sleep(1)
                element.click()

            print(f" {fg}(Success)")

            # Fill contact information
            print(f"{fc}{sd}[{fm}{sb}*{fc}{sd}] {fy}Account Progress - 2/3", end='')

            if not self.safe_send_keys(By.ID, 'inputEmail', email):
                return False
            if not self.safe_send_keys(By.ID, 'inputEmailConfirm', email):
                return False
            if not self.safe_send_keys(By.ID, 'inputSmsPhone', phone):
                return False
            if not self.safe_send_keys(By.ID, 'inputStreetAddress1', street):
                return False
            if not self.safe_send_keys(By.ID, 'inputCity', city):
                return False
            if not self.select_dropdown_option(By.ID, 'inputState', state):
                return False
            if not self.safe_send_keys(By.ID, 'inputPostalCode', postal):
                return False

            time.sleep(2)

            # Submit second page
            if not self.safe_click(By.ID, 'accountFormSubmit'):
                return False

            # Handle phone validation errors
            self.handle_phone_validation(phone)

            print(f" {fg}(Success)")

            # Continue with account creation - simplified version
            print(f"{fc}{sd}[{fm}{sb}*{fc}{sd}] {fy}Account Progress - 3/3", end='')

            # Generate credentials
            username = firstName + str(random.randint(1000000, 9999999))
            password = LastName + str(random.randint(10000, 99999))
            pin = str(random.randint(1000, 9999))

            # Fill credentials
            if not self.safe_send_keys(By.ID, 'inputUserId', username):
                return False
            if not self.safe_send_keys(By.ID, 'inputPasswd', password):
                return False
            if not self.safe_send_keys(By.ID, 'inputPasswdConfirm', password):
                return False
            if not self.safe_send_keys(By.ID, 'inputPin', pin):
                return False
            if not self.safe_send_keys(By.ID, 'inputPinConfirm', pin):
                return False

            # Fill security questions (simplified)
            if not self.select_dropdown_option(By.ID, 'inputSecurityQuestion1', '5'):
                return False
            if not self.safe_send_keys(By.ID, 'inputSecurityAnswer1', LastName + 'ans1'):
                return False

            if not self.select_dropdown_option(By.ID, 'inputSecurityQuestion2', '6'):
                return False
            if not self.safe_send_keys(By.ID, 'inputSecurityAnswer2', LastName + 'ans2'):
                return False

            if not self.select_dropdown_option(By.ID, 'inputSecurityQuestion3', '7'):
                return False
            if not self.safe_send_keys(By.ID, 'inputSecurityAnswer3', LastName + 'ans3'):
                return False

            # Wait for captcha
            print(f"\n{fc}{sd}[{fm}{sb}*{fc}{sd}] {fr}Please solve the captcha in the browser...")

            # Wait for captcha to be solved
            captcha_solved = False
            for i in range(self.config.get('captcha_timeout', 200)):
                try:
                    captcha_input = self.driver.find_element(By.NAME, 'captchaResponse')
                    if captcha_input.get_attribute('value'):
                        captcha_solved = True
                        break
                except:
                    pass
                time.sleep(1)

            if captcha_solved:
                print(f"{fc}{sd}[{fm}{sb}*{fc}{sd}] {fg}Captcha solved, continuing...")

                # Submit final form
                element = self.wait_for_element(By.ID, 'accountFormSubmit')
                if element:
                    self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
                    time.sleep(1)
                    element.click()

                # Save account details
                self.save_account_details(email, password, username, firstName, middle_name, LastName, pin)

                print(f" {fg}(Success)")
                return True
            else:
                print(f"{fc}{sd}[{fm}{sb}*{fc}{sd}] {fr}Captcha timeout")
                return False

        except Exception as e:
            self.logger.error(f"Form filling failed: {e}")
            return False

    def handle_phone_validation(self, phone: str):
        """Handle phone number validation errors"""
        try:
            time.sleep(2)
            error_element = self.driver.find_element(By.ID, 'messageFooterLabel')
            if error_element.is_displayed():
                error_element.click()

                # Retry with new phone number if needed
                retry_count = 0
                while retry_count < 3:
                    phone_input = self.wait_for_element(By.ID, 'inputSmsPhone')
                    if phone_input and 'error' in phone_input.get_attribute('class'):
                        print(f"\n{fc}{sd}[{fm}{sb}*{fc}{sd}] {fr}Invalid phone number, retrying...")
                        new_phone = self.generate_random_phone()
                        phone_input.clear()
                        phone_input.send_keys(new_phone)
                        time.sleep(1)
                        break
                    retry_count += 1
        except:
            pass

    def save_account_details(self, email: str, password: str, username: str,
                           first_name: str, middle_name: str, last_name: str, pin: str):
        """Save generated account details to file"""
        try:
            output_file = self.config.get('output_file', 'generated_accounts.txt')
            birth_date = f"{randomMonth}/{randomDay}/{randomYear}"

            account_info = (
                f"Email: {email}\n"
                f"Password: {password}\n"
                f"Username: {username}\n"
                f"First Name: {first_name}\n"
                f"Middle Name: {middle_name}\n"
                f"Last Name: {last_name}\n"
                f"PIN: {pin}\n"
                f"Birth Date: {birth_date}\n"
                f"Generated: {time.strftime('%Y-%m-%d %H:%M:%S')}\n"
                f"{'-' * 50}\n\n"
            )

            with open(output_file, 'a', encoding='utf-8') as f:
                f.write(account_info)

            print(f"{fc}{sd}[{fm}{sb}*{fc}{sd}] {fg}Account details saved to {output_file}")

        except Exception as e:
            self.logger.error(f"Failed to save account details: {e}")

if __name__ == "__main__":
    generator = EduMailGenerator()
    generator.run()
