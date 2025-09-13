import requests
import json
import pandas as pd

from requests import RequestException


def get_currencyes(cur_url):  #Получаем словарь валюты по API
    try:
        response = requests.get(cur_url)
        return response.json()
    except RequestException as err:
        print(f"Ошибка запроса {err}")
        return None


def write_to_file(currency_dict):   # Бэкап в json формате
    with open("currency.json", "w") as f:
        json.dump(currency_dict, f, indent=2)

def transform_to_df(currency):  #Парсим в pandas.DataFrame
    data = currency['conversion_rates']
    df = pd.DataFrame(list(data.items()), columns=['Currency', 'Rate_to_USD'])
    return  df

def transform_to_csv(cur_df):  #Записываем в .csv
    cur_df.to_csv("currencyes.csv", index=False)


def main():
    api_key = "87fbf054dc51175d0b1e67bd"
    url = f"https://v6.exchangerate-api.com/v6/{api_key}/latest/USD"

    currencyes = get_currencyes(url)
    write_to_file(currencyes)
    currencyes_df = transform_to_df(currencyes)
    print(currencyes_df)

    transform_to_csv(currencyes_df)


if __name__ == "__main__":
    main()
