from selenium import webdriver
from selenium.common.exceptions import WebDriverException
import data
import json
import time
import random

def get_browser_driver():
    # Get the proper browser.path
    import platform

    os_name = platform.system()

    if os_name == 'Linux':
        driver_path = 'linux/chromedriver'
    elif os_name == 'Darwin':
        driver_path = 'mac/chromedriver'
    elif os_name == 'Windows':
        driver_path = 'win/chromedriver.exe'
    else:
        raise NotImplementedError("Not supported on this operating system!")

    return 'driver/chrome/{}'.format(driver_path)

def create_browser():
    return webdriver.Chrome(get_browser_driver())

def visit():
    browser = create_browser()
    ants = get_ants()
    bosses = get_bosses()
    login_url = 'https://i.qq.com'
    boss_url = 'https://user.qzone.qq.com/{}'

    try:
        for ant in ants:
            browser.get(login_url)
            browser.switch_to.frame('login_frame')
            browser.find_element_by_id('switcher_plogin').click()
            browser.find_element_by_id('u').clear()
            browser.find_element_by_id('u').send_keys(ant.__name__)
            browser.find_element_by_id('p').clear()
            browser.find_element_by_id('p').send_keys(ant.__password__)
            browser.find_element_by_id('login_button').click()

            skip = False

            for boss in bosses:
                browser.get(boss_url.format(boss.__name__))

                # check if log in successfully
                try:
                    browser.find_element_by_id('QM_OwnerInfo_Icon')
                except WebDriverException:
                    skip = True
                    break

                try:
                    browser.find_element_by_class_name('btn-fs-sure').click()
                except WebDriverException:
                    pass

                print(ant.__name__, 'has visited', boss.__name__)

            if skip:
                print(ant.__name__, 'may have wrong password', ant.__password__)
                continue

            time.sleep(random.randrange(1,4))
            browser.find_element_by_id('tb_logout').click()
            alert = browser.switch_to_alert()
            alert.accept()
            time.sleep(random.randrange(1,4))

    except WebDriverException as e:
        print(e)
        print(ant, boss)
        browser.quit()
    else:
        browser.quit()

def check_config(path):
    from pathlib import Path

    assert Path(path).exists(), path + ' does not exist!'

def get_ants(path = 'config/ants.json'):
    check_config(path)

    with open(path, 'r', encoding = 'utf-8') as ants_config:
        ants = json.load(ants_config, cls = data.QQDecoder)

    return ants

def get_bosses(path = 'config/bosses.json'):
    check_config(path)

    with open(path, 'r', encoding = 'utf-8') as bosses_config:
        bosses = json.load(bosses_config, cls = data.QQDecoder)

    return bosses

if __name__ == '__main__':
    visit()
