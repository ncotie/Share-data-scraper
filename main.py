from Classes.CSV import CSV
from Classes.StockIndex import StockIndex
import sys


if __name__ == "__main__":

    # Here we list the Indices for which the scraping program should work.
    # Note that several are excluded for having too many components to fit
    # into the SIX Webpage table in one pane.
    # The scraper has not been coded to be able to step through more than one pane
    # of this components table.
    valid_indices = ['SMI',
                     'SMI-MID',
                     'SLI',
                     'SPI-20',
                     'SXI-Switzerland-Sustainability-25',
                     ]

    # Absorb command line arguments, which should only be two strings,
    # one being one of the accepted Swiss market SIX index names,
    # the second being a Boolean to indicate whether it is acceptable
    # to scrape data during an open market, or not.
    if len(sys.argv) > 3:
        print("Program can only accept one Index name per run, followed by Boolean value, \n"
              "to specify whether market data may be scraped during market open hours, or not.")
        sys.exit("Program terminating.")
    [index, open_market_ok_string] = sys.argv[1:]
    # Need to convert True / False string to a boolean
    open_market_ok = open_market_ok_string == "True"
    if index not in valid_indices:
        print("Index {} is either not a valid index name, or cannot be scraped by this program.\n"
              "Program can work with the following indices:\n"
              "{}".format(index, ', '.join(valid_indices)))
        sys.exit("Program terminating.")

    # Note: below page is a base URL but is not directly browsable.
    # The program could be extended to take this as an argument also
    page = "https://www.six-group.com/en/products-services/the-swiss-stock-exchange/market-data/"

    # Instantiate StockIndex object and store reference
    stock_index_object_ref = StockIndex(index, page)

    # Request StockIndex object to scrape its components' data
    result, scraped_date, return_stock = stock_index_object_ref.scrape(open_market_ok)
    if result == 0:
        print("Scraping completed successfully, data collected for date {}.".format(scraped_date))
    else:
        # if not successful, print textual message of what happened, during which stock, if applicable
        print("Scraping not completed, the following problem occurred during scraping for {}:"
              "\n{}".format(return_stock, result, ))
        sys.exit("Program terminating.")

    # Store data via CSV and JSON objects
    path = "Logfiles/"
    filename = "{}_scraped_data".format(index)
    CSV_object_ref = CSV(path, filename, stock_index_object_ref)
    result = CSV_object_ref.update_csv_file()
    if result == 0:
        print("Storage of scraped data into CSV format completed.")
    else:
        print(result)
        print("Attempting storage to JSON file.")


    #JSON_object_ref = JSON(path, filename)
    #result = JSON_object_ref.update_json_file()
    #if result == 0:
    #    print("Storage of scraped data into JSON format completed.")
    #else:
    #    print(result)
    #    sys.exit("Program terminating.")
