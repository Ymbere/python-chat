import csv

import pandas as pd
import requests


class StockFetcher():
    def __init__(self):
        pass

    def prepera_message(self, stock_price, stock_name):
        stock_name = stock_name.upper()
        if stock_price != 'N/D':
            message = "{} quote is ${} per share".format(
                stock_name, stock_price)
            return message
        else:
            message = "Could not find the price for the stock {}".format(
                stock_name)
            return message

    def get_stock_code_from_message(self, message):
        message = message.rstrip("\n")
        message_list = message.split('=')
        stock_code = message_list[-1]

        return stock_code

    def get_stock_price(self, download_csv):
        csv_to_list = list(download_csv)
        stock_data_frame = pd.DataFrame(
            csv_to_list[1:], columns=csv_to_list[0]
        )
        prices = stock_data_frame['Open'].values
        price = prices[-1]

        return price

    def download_csv(self, stock_name):
        stock_name = stock_name.lower()

        api_url = "https://stooq.com/q/l/?s={}&f=sd2t2ohlcv&h&e=csv".format(
            stock_name)

        downloaded_csv = requests.get(api_url)
        downloaded_csv = downloaded_csv.content.decode('utf-8')
        csv_parsed = csv.reader(downloaded_csv.splitlines(), delimiter=',')

        return csv_parsed

    def fetch_stock_information(self, message):
        stock_name = self.get_stock_code_from_message(message)
        csv = self.download_csv(stock_name)
        stock_price = self.get_stock_price(csv)
        information = self.prepera_message(stock_price, stock_name)

        return information
