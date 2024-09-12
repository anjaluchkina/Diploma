from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time
import json

user_agent = ('Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 '
              '(KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36')

chrome_option = Options()
chrome_option.add_argument(f'user-agent={user_agent}')
chrome_option.add_argument('start-maximized')

driver = webdriver.Chrome(options=chrome_option)
url = 'https://rushandball.ru/publications'

try:
    driver.get(url)
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))

    scroll_pause = 2
    page_height = driver.execute_script('return document.documentElement.scrollHeight')
    while True: # Цикл прокрутки
        driver.execute_script('window.scrollTo(0, document.documentElement.scrollHeight);')
        time.sleep(scroll_pause)
        new_height = driver.execute_script('return document.documentElement.scrollHeight')
        if new_height == page_height:
            break
        page_height = new_height

    articles_data = [] # Для хранения основного списка статей
    articles_info = [] # Для хранения данных из статей

    while True:
        try:
            article_titles = driver.find_elements(By.XPATH, "//*[@id='pubs-wrapper']/div/article/div[1]//div/a")
            metadata_elements = driver.find_elements(By.XPATH, "//*[@id='pubs-wrapper']/div/article/div[2]/div[2]")
            published_elements = driver.find_elements(By.XPATH, "//*[@id='pubs-wrapper']/div/article/div[2]/div[1]")
            break
        except Exception as e:
            print(f'Ошибка при извлечении элементов списка: {e}')
            time.sleep(2)

    for i in range(min(len(article_titles), len(metadata_elements), len(published_elements))):
        title = article_titles[i].text
        view = metadata_elements[i].text
        time_ago = published_elements[i].text
        article_link = article_titles[i].get_attribute('href')

        # Сохраняем основные данные статьи в articles_data
        articles_data.append({
            'title': title,
            'views': view,
            'published_date': time_ago,
            'link': article_link
        })

        driver.get(article_link)  # Переход на страницу статьи
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))

        try:
            name_title = driver.find_element(By.XPATH, '/html/body/div[2]/section/div/div[3]/div/h1').text
            article = driver.find_element(By.XPATH, '/html/body/div[2]/section/div/div[4]/article').text
            article_title = driver.find_element(By.XPATH, '/html/body/div[2]/section/div/div[4]/article/div[1]').text
            article_subtitle = driver.find_element(By.XPATH, '/html/body/div[2]/section/div/div[4]/article/p/strong').text

            # Сохраняем извлеченные данные из статьи в articles_info
            articles_info.append({
                'title': title,  
                'name_title': name_title,
                'article': article,
                'article_title': article_title,
                'article_subtitle': article_subtitle
            })
        except Exception as e:
            print(f'Ошибка при извлечении данных из статьи: {e}')

        driver.back()  # Возврат к списку статей
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))

        # Обновляем список статей
        article_titles = driver.find_elements(By.XPATH, "//*[@id='pubs-wrapper']/div/article/div[1]//div/a")
        metadata_elements = driver.find_elements(By.XPATH, "//*[@id='pubs-wrapper']/div/article/div[2]/div[2]")
        published_elements = driver.find_elements(By.XPATH, "//*[@id='pubs-wrapper']/div/article/div[2]/div[1]")

    # Сохранение данных в JSON файлы
    with open('article_data.json', 'w', encoding='UTF-8') as f:
        json.dump(articles_data, f, ensure_ascii=False, indent=4)

    with open('article_information.json', 'w', encoding='UTF-8') as f:
        json.dump(articles_info, f, ensure_ascii=False, indent=4)

    print('Данные о статьях сохранены в файл article_data.json')
    print('Данные из статей сохранены в файл article_information.json')

except Exception as e:
    print(f'Произошла ошибка: {e}')
finally:
    driver.quit()