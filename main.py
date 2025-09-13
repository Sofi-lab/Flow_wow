import requests
import pandas as pd
import json


api_key = "87fbf054dc51175d0b1e67bd"
url = f"https://v6.exchangerate-api.com/v6/{api_key}/latest/USD"


response = requests.get(url)
result = response.json()

# Бэкап в json формате
with open("currency.json", "w") as f:
    json.dump(result, f, indent=2)

currency = result['conversion_rates'] #Получили словарь с валютой

df = pd.DataFrame(list(currency.items()), columns = ['Currency', 'Rate_to_USD']) #Преобразуем в DF

df.to_csv("currencyes.csv", index=False)

