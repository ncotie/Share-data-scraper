from Classes.Stock import Stock
from Classes.StockIndex import StockIndex
import os

# JSON work incomplete due to lack of time

class JSON:
    """
    Implements a class to represent JSON format file storage for scraped Stock data.
    """
    def __init__(self, path, filename, stock_index):
        """
        Constructor for JSON class
        :param path: relative path to file storage
        :param filename: filename, without suffix
        :param stock_index: reference to StockIndex object
        """
        self.path = path
        self.filename = filename
        self.stockIndex = stock_index

    def update_json_file(self):
        """
        Triggers the creation or updating of a JSON file on the OS
        that stores the scraped data for the StockIndex in question.
        :return:
        """


