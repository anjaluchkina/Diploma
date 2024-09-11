from selenium import webdriver
from selenium.webdriver.chrome.options import Options

user_agent = (
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 '
    '(KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36'
)

chrome_option = Options()
chrome_option.add_argument(f'user-agent={user_agent}')
# chrome_option.add_argument('--ignore-certificate-errors-spki-list')
chrome_option.add_argument('start-maximized')  # хром на весь экран

driver = webdriver.Chrome(options=chrome_option)
driver.get('https://example.com')

# Извлечение названия страницы
title = driver.title
print(title)
driver.quit()