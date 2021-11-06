

from Classes.StockIndex import StockIndex

# Note: below page is a base URL but is not directly browsable.
page = "https://www.six-group.com/en/products-services/the-swiss-stock-exchange/market-data/"

# Hard coded for now, should be spread into a List of indices available at SIX
index = "SMI"


####  HOW DO I GET ARGUMENTS OF THE USER'S CALL INTO PYTHON ???

if __name__ == "__main__":

    # Instantiate StockIndex object and store reference
    stock_index_object_ref = StockIndex(index, page)

    # is it acceptable to scrape market data while market is open, or not
    open_market_ok = True

    ### Need to see how to get open_market_ok from the user call

    # Request StockIndex object to scrape its components' data
    result, scraped_date, return_string = stock_index_object_ref.scrape(open_market_ok)
    if result == 0:
        print("Scraping completed successfully, data collected for date {}.".format(scraped_date))
    else:
        # if not successful, print textual message of what happened, during which stock, if applicable
        print("Scraping not completed, {} occurred during scraping for {}.".format(result, return_string))

        #######  Note that full Stock objects not instantiated, even if an error is encountered
        #####  Need to skip any storage if an error occurs, work out how.

    # Store data via CSV and JSON objects
    path = "Logfiles/"
    filename = "{}_scraped_data".format(index)
    #CSV_object_ref = CSV(path, filename)
    #JSON_object_ref = JSON(path, filename)

