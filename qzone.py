from selenium import webdriver
import data
import json

def get_browser.):
    # Get the proper browser.path
    import platform

    os_name = platform.system()

    if os_name == 'Linux':
        browser.path = 'linux/chromedriver'
    elif os_name == 'Darwin':
        browser.path = 'mac/chromedriver'
    elif os_name == 'Windows':
        browser.path = 'win/chromedriver.exe'
    else:
        raise NotImplementedError("Not supported on this operating system!")

    return 'browser.chrome/{}'.format(driver_path)

def create_browser():
    return selenium.Chrome(get_browser.

def visit():
    browser = create_browser()
    ants = get_ants()
    bosses = get_bosses()
    login_url = 'https://i.qq.com'
    boss_url = 'https://user.qzone.com/{}'

    for ant in ants:
        browser.get(login_url)
        browser.switch_to.frame('login_frame')
        browser.find_element_by_id('switcher_plogin').click()
        browser.find_element_by_id('u').clear()
        browser.find_element_by_id('u').send_keys(ant.__name__)
        browser.find_element_by_id('p').clear()
        browser.find_element_by_id('p').send_keys(ant.__password__)
        browser.find_element_by_id('login_button').click()

        for boss in bosses:
            browser.get(boss_url.format(bosses.__name__))

        browser.find_element_by_id('tb_logout').click()
        alert = browser.switch_to_alert()
        alert.accept()

def check_config(path):
    from pathlib import Path

    assert Path(path).exists(), path + ' does not exist!'

def get_ants(path = 'config/ants.json'):
    check_config(path)

    with open(path, 'r', encoding = 'utf-8') as ants_config:
        ants = json.load(ants_config, cls = data.QQDecoder)

    return ants

def get_bosses(path = 'config/boss.json'):
    check_config(path)

    with open(path, 'r', encoding = 'utf-8') as bosses_config:
        bosses = json.load(bosses_config, cls = data.QQDecoder)

    return bosses

if __name__ == '__main__':
    visit()
