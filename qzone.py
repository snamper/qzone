from selenium import webdriver
from selenium.common.exceptions import WebDriverException
import data
import json
import time
import random
import logging, logging.config

def get_browser_driver():
    '''Get the proper browser.path'''
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
    '''Get a new browser'''
    return webdriver.Chrome(get_browser_driver())

def visit():
    browser = create_browser()
    logger.info('Browser created successfully.')

    ants = get_ants()
    logger.info('{} ants loaded.'.format(len(ants)))

    bosses = get_bosses()
    logger.info('{} bosses loaded.'.format(len(bosses)))

    login_url = 'https://i.qq.com'
    boss_url_formatter = 'https://user.qzone.qq.com/{}'

    for ant in ants:
        if login(browser, ant, login_url):
            sleep_random()

            for boss in bosses:
                boss_url = boss_url_formatter.format(boss.__name__)
                visit_boss(browser, ant, boss, boss_url)

        logout(browser, ant, login_url)

    browser.quit()

def visit_boss(browser, ant, boss, boss_url):
    '''Visit boss'''
    visited, counter, max_times= False, 0, 4

    while not visited and counter < max_times:
        browser.get(boss_url)
        close_help_page(browser)
        sleep_random(1000, 1500)
        browser.refresh()

        visited = has_visited(browser)
        counter += 1

    if visited:
        logger.info('{0} has visited {1} successfully.'.format(ant.__name__, boss.__name__))
    else:
        logger.warn('{0} can not visit {1} after \
            trying {2} times.'.format(ant.__name__, boss.__name__, max_times))

def login(browser, ant, login_url):
    '''Log in Qzone'''
    import vlc

    name, password = ant.__name__, ant.__password__
    browser.get(login_url)
    browser.switch_to.frame('login_frame')
    browser.find_element_by_id('switcher_plogin').click()
    browser.find_element_by_id('u').clear()
    browser.find_element_by_id('u').send_keys(name)
    browser.find_element_by_id('p').clear()
    browser.find_element_by_id('p').send_keys(password)
    browser.find_element_by_id('login_button').click()
    sleep_random()

    counter, max_times = 0, 3
    while not has_logged_in(browser) and counter < max_times:
        logger.warn('{} needs to be verified!'.format(name))
        notify_path = 'voice/notify_verify.mp3'
        player = vlc.MediaPlayer(notify_path)
        player.play()
        time.sleep(15)
        player.release()
        counter += 1

    if counter == max_times:
        return False

    # close_help_page(browser)

    logger.info('{} has logged in successfully.'.format(name))

    return True

def close_help_page(browser):
    '''Close the help page if existing'''
    try:
        browser.find_element_by_class_name('btn-fs-sure').click()
    except WebDriverException:
        pass

def has_visited(browser):
    '''Check if visiting'''
    try:
        browser.find_element_by_id('QM_OwnerInfo_Icon')
        return True
    except WebDriverException:
        return False

def has_logged_in(browser):
    '''Check if log in'''
    has_vcode, has_info = False, False

    try:
        browser.find_element_by_id('newVcodeArea')
        has_vcode = True
    except WebDriverException:
        pass

    sleep_random(1000, 2000)

    try:
        browser.find_element_by_id('QM_OwnerInfo_Icon')
        has_info = True
    except WebDriverException:
        pass

    return has_vcode or has_info

def logout(browser, ant, logout_url):
    '''Log out Qzone'''
    #logger.info("It's logging out.")
    while True:
        browser.get(logout_url)
        if has_logged_in(browser):
            try:
                browser.find_element_by_id('tb_logout').click()
                alert = browser.switch_to_alert()
                alert.accept()
                break
            except WebDriverException:
                pass
        else:
                break

    logger.info('{} has logged out successfully.'.format(ant.__name__))

def check_config(path):
    '''Check if the config file exists'''
    from pathlib import Path

    assert Path(path).exists(), path + ' does not exist!'

def get_ants(path = 'config/ants.json'):
    '''Get working ants from json'''
    check_config(path)

    with open(path, 'r', encoding = 'utf-8') as ants_config:
        ants = json.load(ants_config, cls = data.QQDecoder)

    return ants

def get_bosses(path = 'config/bosses.json'):
    '''Get bosses from json'''
    check_config(path)

    with open(path, 'r', encoding = 'utf-8') as bosses_config:
        bosses = json.load(bosses_config, cls = data.QQDecoder)

    return bosses

def sleep_random(lower = 200, upper = 500):
    '''Sleep randomly from 200 ms to 500 ms'''
    time.sleep(random.randrange(lower, upper) / 1000)

# Logger
logging.config.fileConfig('config/logging.config')
logger = logging.getLogger('simpleExample')

if __name__ == '__main__':
    visit()
