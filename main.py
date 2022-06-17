
from time import sleep
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import pyautogui
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from tqdm import tqdm

class Custom_Errors:
    class DriverNotInitiated(Exception):
        '''
        driver not initialised
        '''
    class InvalidPhoneNumber(Exception):
        '''
        Phone number is not valid
        '''
    class InvalidTimeError(Exception):
        '''
        Invalid time has been passed
        '''


class Automation(Custom_Errors):

    def __init__(self) -> None:
        self.driver = None
        self.url: str = f'https://web.whatsapp.com/send?phone='

    def initiate(
        self,
        Maximise_window: bool = False
    ) -> None:

        self.service = Service(
            ChromeDriverManager().install()
        )

        self.Maximise_window: bool = Maximise_window

    def send_a_message(
        self,
        PhoneNumber: str | int,
        countrycode: str = +91,
        message: str = None,
        Hour: int = 0,
        Minute: int = 0,
        seconds: int = 0,
        delay: int = 60
    ):
        if not (0 <= Hour <= 24 and 0 <= Minute <= 60 and 0 <= seconds <= 60):
            raise Custom_Errors.InvalidTimeError
        now = datetime.now()
        flowtime = now
        flowtime = flowtime.replace(
            hour=Hour,
            minute=Minute,
            second=seconds,
            microsecond= 0,
        )
        if now > flowtime:
            raise Custom_Errors.InvalidTimeError
        else:
            waitfor = flowtime - now
            print(waitfor.seconds)
            for i in tqdm(range(waitfor.seconds)):
                sleep(1)
            # sleep(waitfor.seconds)
        if isinstance(PhoneNumber, int):
            PhoneNumber = str(PhoneNumber)

        if len(PhoneNumber) != 10:
            raise Custom_Errors.InvalidPhoneNumber
        try:
            # self.driver = webdriver.Chrome(
            #     service=Service(ChromeDriverManager().install()))

            options = webdriver.ChromeOptions()
            options.add_experimental_option('excludeSwitches', ['enable-logging'])
            self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=options)

            self.driver.maximize_window() if self.Maximise_window else None

            

            self.driver.get(
                url=(str(self.url) + str(countrycode) + str(PhoneNumber)
                     )
            )

            WebDriverWait(
                self.driver,
                delay).until(
                EC.presence_of_element_located(
                    (
                        By.ID,
                        'main'
                    )
                )
            )
            sleep(10)
            if message is not None:
                pyautogui.write(
                    message=message,
                )
            sleep(1)
            pyautogui.press('enter')
            

        except Exception as E:
            print(E)

    def quit(self):
        pyautogui.alert("Message sent successfully!")
        if self.driver is None:
            raise Custom_Errors.DriverNotInitiated("Driver Not found")
        else:
            self.driver.quit()


