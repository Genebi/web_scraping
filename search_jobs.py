from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

def search_and_get_url(job, location=None):
    
    url = 'https://mx.indeed.com/'
    
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_experimental_option("detach", True)
    browser = webdriver.Chrome(options=chrome_options, service=Service(ChromeDriverManager().install()))
    # browser.maximize_window()
    browser.get(url)
    
    browser.implicitly_wait(5);
    
    search_input = browser.find_element(By.ID, 'text-input-what')
    where_input = browser.find_element(By.ID, 'text-input-where')
    
    if job != None and location == None:
        search_input.send_keys(job, Keys.RETURN)
        browser.implicitly_wait(5)
    else:
        search_input.send_keys(job)
        browser.implicitly_wait(5)
        where_input.send_keys(location, Keys.RETURN)
    
    browser.implicitly_wait(5)
    current_url = browser.current_url
    
    browser.close()
    browser.quit()
    
    # print(current_url)
    return current_url

if __name__ == '__main__':
    search_and_get_url()
    