from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import json

# Инициализация драйвера Selenium
driver = webdriver.Chrome()
url = 'https://www.youtube.com/@progliveru/videos'
driver.get(url)

try:
    # Ожидание загрузки элементов на странице
    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
    for _ in range(5):  # Прокрутка страницы
        driver.execute_script('window.scrollTo(0, document.documentElement.scrollHeight);')
        time.sleep(2)

    # Извлечение данных с динамической страницы
    titles = driver.find_elements(By.XPATH, "//*[@id='video-title-link']")
    metadata = driver.find_elements(By.XPATH, "//div[@id='metadata-line']/span[1]")
    published = driver.find_elements(By.XPATH, "//div[@id='metadata-line']/span[2]")

    video_data = {titles[i].text: {'views': metadata[i].text.strip(), 'published': published[i].text.strip()} 
                   for i in range(len(titles))}

    # Сохранение данных в JSON формате
    with open('video_data.json', 'w', encoding='UTF-8') as json_file:
        json.dump(video_data, json_file, ensure_ascii=False, indent=4)
    print('Данные сохранены в video_data.json')

except Exception as e:
    print(f'Ошибка: {e}')

finally:
    # Закрытие браузера
    driver.quit()