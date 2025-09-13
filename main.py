import requests
import json
import pandas as pd
import logging

from requests import RequestException

logging.basicConfig(level=logging.INFO, filename="journal_log.log",filemode="w",
                    format="%(asctime)s %(levelname)s %(message)s") #Конструктор: начинаем с уровня INFO  с временными метками
logging.debug("A DEBUG Message")
logging.info("An INFO")
logging.warning("A WARNING")
logging.error("An ERROR")
logging.critical("A message of CRITICAL severity")



def get_currencyes(cur_url):  #Получаем словарь валюты по API
    logging.info(f"Request = {cur_url}")
    try:
        response = requests.get(cur_url)
        data = response.json()

        if data.get("result") == "error":
            logging.error(f"API result = {data}")
            return None
        else:
            return data
    except RequestException as err:
        logging.exception("Request Error", exc_info=True)
        return None


def write_to_file(currency_dict):   # Бэкап в json формате
    logging.info(f"Write to file")
    if currency_dict is None:
        logging.error(f"Currency dict is none")
        return
    else:
        logging.info(f"Saving {len(currency_dict.get('conversion_rates', {}))} data currencyes in currency.json")
        with open("currency.json", "w") as f:
            json.dump(currency_dict, f, indent=2)


def transform_to_df(currency):  #Парсим в pandas.DataFrame
    logging.info("Tranform to df")

    if currency is not None:
        data = currency['conversion_rates']
        df = pd.DataFrame(list(data.items()), columns=['Currency', 'Rate_to_USD'])
        logging.info(f"Created DataFrame with {df.shape[0]} rows")
        return  df
    else:
        logging.error(f"Currency data is empty, can not create data frame")
        return

def transform_to_csv(cur_df):  #Записываем в .csv
    logging.info("Transform to csv")
    if cur_df is None:
        logging.error(f"Empty data frame")
        return
    else:
        cur_df.to_csv("currencyes.csv", index=False)
        logging.info("Csv file created success")


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
