from bs4 import BeautifulSoup

html_doc = """
<html>
<head>
<title>Мой сайт</title>
</head>
<body>
<h1>Добро пожаловать на сайт!</h1>
<p>This is a paragraph of text.</p>
<a href="https://www.example.com">Click me</a>
</body>
</html>
"""

# Создаем объект BeautifulSoup
soup = BeautifulSoup(html_doc, 'html.parser')

# Ищем элементы
title = soup.title.string
heading = soup.h1.string
link = soup.a['href']

# Выводим данные
print("Название:", title)  # Название: Моя веб-страница
print("Заголовок:", heading)  # Заголовок: Добро пожаловать на мой сайт
print("Ссылка:", link)  # Output: Ссылка: https://www.example.com