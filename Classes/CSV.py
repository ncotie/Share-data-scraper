from Classes.Stock import Stock
from Classes.StockIndex import StockIndex
import os


class CSV:
    """
    Implements a class to represent CSV format file storage for scraped Stock data.
    """
    def __init__(self, path, filename, stock_index):
        """
        Constructor for CSV class
        :param path: relative path to file storage
        :param filename: filename, without suffix
        :param stock_index: reference to StockIndex object
        """
        self.path = path
        self.filename = filename
        self.stockIndex = stock_index

    def update_csv_file(self):
        """
        Triggers the creation or updating of a CSV file on the OS
        that stores the scraped data for the StockIndex in question.
        :return:
        """

        def assemble_csv_line(*args):
            """
            Nested function to assemble a line of data into CSV format
            with double quotes on each element and comma as separator,
            with trailing \n newline.
            :param args: a set of arguments to assemble, either strings or lists of strings
            :return: line, the assembled string
            """
            line = ""
            for x in args:
                if type(x) == str:
                    if line != "":
                        line = line + ',' + '\"' + x.replace('\n', '') + '\"'
                    else:
                        line = '\"' + x.replace('\n', '') + '\"'
                elif type(x) == list:
                    if line != "":
                        line = line + ',' + '\"' + '\",\"'.join(x).replace('\n', '') + '\"'
                    else:
                        line = '\"' + '\",\"'.join(x).replace('\n', '') + '\"'
            line = line + '\n'
            return line

        # Fetch the Stock object reference list that makes up the StockIndex
        stock_object_dict = self.stockIndex.get_component_stock_objects()
        # Fetch scraped Stock data for first object, to assemble a header row
        stock_data = list(stock_object_dict.values())[0].get_data()
        # Call nested function to assemble the header
        header = assemble_csv_line("Date", "Stock name",
                                   list(stock_data[2].keys()),
                                   list(stock_data[3].keys()),
                                   list(stock_data[4].keys()),
                                   list(stock_data[5].keys())
                                   )

        # Check if CSV file exists on OS already   NOTE: path is relative
        file_path = os.path.join(self.path, self.filename + ".csv")

        try:
            if not os.path.isdir(self.path):
                # if directory does not exist, create it
                os.mkdir(self.path)
            if os.path.exists(file_path):
                # if file already exists check against its header row, and that scraped date is new
                with open(file_path, 'r') as f:
                    file_header_row = f.readline()
                    # Need to ensure the existing header column names match the new data
                    if not file_header_row == header:
                        return "Mismatched header: " \
                               "verify if stock data has changed from that previously stored in CSV file." \
                            "\nStorage of scraped data aborted."
                    # Need to fetch last entered date to see if the scraped data is a following date
                    # or the same date.  If the same, return an error message.
                    for line in f:
                        pass
                    if stock_data[0] == line[1:11]:   # slice only the date without quotes out of csv line
                        # Then dates match, need to raise error message
                        return "Scraped dates are equal to last date stored in CSV file.  " \
                               "\nStorage of scraped data aborted."
                    # At this point we allow the file object to be closed.
            else:   # if file did not exist we need to write in the header
                try:
                    with open(file_path, 'w') as f:
                        f.write(header)
                except Exception:
                    return "Error creating the CSV file."
        # If any file operation Exception is raised above, return error message
        except Exception:
            return "Error accessing CSV file specified."

        # Checks have been done, proceed with fetching of each Stock's scraped data,
        # formatting it into a CSV line, and appending it to the file
        try:
            with open(file_path, 'a') as f:  # 'a' append mode will create file if doesn't exist
                for stock in list(stock_object_dict.values()):
                    # for each Stock call get_data to fetch the stored scraped data
                    # in a list form, with stock name, date, and 4 data dictionaries as elements
                    stock_data = stock.get_data()
                    csv_line = assemble_csv_line(
                        stock_data[0],      # Date
                        stock_data[1],      # Stock name
                        list(stock_data[2].values()),   # Sets of data
                        list(stock_data[3].values()),
                        list(stock_data[4].values()),
                        list(stock_data[5].values()))
                    f.write(csv_line)
            # Writing to CSV completed upon finishing iteration loop and exiting 'with open' structure.
            # Return zero as "successful" to caller
            return 0
        except Exception:
            return "Error writing to CSV file."
