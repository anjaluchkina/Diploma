import requests
import json

# API Credentials
client_id = "__"
client_secret = "__"
endpoint = "https://api.foursquare.com/v3/places/search"

# Input city and venue type
city = input("Введите город: ")
final_dest = input("Введите заведение: ")
params = {"near": city, "query": final_dest}
headers = {"Accept": "application/json", "Authorization": "токен"}

# API Request
response = requests.get(endpoint, params=params, headers=headers)

# Handle response
if response.status_code == 200:
    venues = response.json()["results"]
    for venue in venues:
        print(f"Название: {venue['name']}, Адрес: {venue['location'].get('address', 'Не найден')}")
else:
    print("Ошибка:", response.status_code)