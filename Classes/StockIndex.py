import time

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

from Classes.Stock import Stock


class StockIndex:
    """
    Implements a single stock (share issued by a company) object
    for the purpose of the data scraper.
    A stock is a component of a stockIndex.
    """
    def __init__(self, index_name, market_url):
        """
        Constructor for class StockIndex
        :param index_name: name of the stock market index
        :param market_url: URL pointing to the market data web page
        """
        self.index_name = index_name
        self.market_url = market_url
        # Dict to hold the stock components, key is stock name, value is url for stock
        self.component_stocks = {}
        # Dict to hold the stock Object references, key is stock name, value is stock object reference
        self.component_stock_objects = {}

        # Note: one could also do the collecting of the index components
        # here in the constructor, with a separate Webdriver.
        # However, to keep the Webdriver handling simpler, we will do it
        # when scrape() is ordered.

    def scrape(self, open_market_ok):
        """
        Request to scrape data for all index component stocks.
        Begins by collecting the index component stocks, triggering the
        instantiation of Stock Objects and requesting each to scrape their
        own data.
        Function uses selenium.Webdriver, controls its opening and closing.
        :param open_market_ok: Boolean, does operator desire data scraping even if market
        not closed yet.
        :return: result
        """

        def fetch_components(driver, index_url):
            """
            Nested function to manage the collection of the index components
            from the market data web site already stored.
            :type driver: selenium Webdriver
            :param driver: The opened selenium.Webdriver to use
            :param index_url: The assembled URL for the market data page for this index
            :return: component_dict: A dictionary of the component stock names and data URLs
            """
            # Prepare data structures
            component_list_tags = []  # where we store the tags we want, of the Index Component names and URLs

            # Use provided selenium webdriver to read the index components list
            try:
                driver.get(index_url)
            except Exception:
                return "Problem opening Web site"

            # Enclose all tag searching inside try / except to catch any Exceptions
            try:
                # Accept cookies after a pause, by clicking on button
                WebDriverWait(driver, 10).until(
                    ec.element_to_be_clickable((By.ID, "onetrust-accept-btn-handler"))).click()

                # First expand the Index Components table on page
                time.sleep(8)
                driver.find_element(By.CLASS_NAME, "expander-trigger").click()

                # Now fetch the tags we want, first the row levels
                component_rows_tags = driver.find_element(By.CLASS_NAME, "expander-body")\
                    .find_elements(By.CLASS_NAME, "rt-tr-group")
                # For each table row, isolate the <a> tag and collect
                for rowTag in component_rows_tags:
                    component_list_tags.append(rowTag.find_element(By.TAG_NAME, "a"))
                # From the <a> tags, get the text and href, and arrange into dict with Stock name as key,
                # using dictionary comprehension.
                component_dict = {component_list_tags[x].text: component_list_tags[x].get_attribute('href')
                                  for x in range(len(component_list_tags))}
            except Exception:
                return "Problem parsing Index Component tags."
            print("The {} index has {} components.".format(self.index_name, len(component_dict)))
            # should be 20 for SMI

            return component_dict
            # -------- End of nested function ---------- #

        # Prepare URL to access to collect components
        # need to change Index name to lower case
        equity_indices_url_suffix = "/indices/equity-indices/{}.html".format(self.index_name.lower())
        index_url = self.market_url + equity_indices_url_suffix

        # Instantiate Options class to allow for headless browser
        options = Options()
        options.headless = True

        # Instantiate Webdriver
        driver = webdriver.Firefox(options=options)

        # Inside a try - finally, execute all scraping then finally close Webdriver
        try:
            # Call nested function to collect Stock components from market website
            component_stocks = fetch_components(driver, index_url)
            if type(component_stocks) != dict:  # Then an error has happened
                return component_stocks, "", ""  # i.e. if a string is returned instead, pass it back
            # if a dict as expected, store into Instance data
            self.component_stocks = component_stocks

            # Now that we have the components, create Stock object for each one,
            # and request each, in turn, to use the Webdriver to scrape their data.
            # Their data remains in their own Stock object, and they remain active.

            for component, url in component_stocks.items():
                # Create Stock and store object reference
                time.sleep(10)
                stock = Stock(component, url)
                self.component_stock_objects[component] = stock
                stock_scrape_result, scraped_date = stock.scrape_data(driver, open_market_ok)
                if stock_scrape_result != 0:  # if result is not ok, break the loop with return
                    return stock_scrape_result, scraped_date, component
                # Note that if an error is encountered, we will never build out the complete set of Stock objects.

                # print to say which stock has been scraped, and count of total
                print("Data scraped for {}, for date {}, {}/{}".format(component,
                                                                       scraped_date,
                                                                       len(self.component_stock_objects),
                                                                       len(self.component_stocks)))

            return 0, scraped_date, "All"  # if successful
        finally:
            # Need to close the Webdriver, no longer needed, all scraping is done.
            driver.quit()

    def get_component_stock_objects(self):
        """
        Fetches the dictionary of stock names and Stock object references that make up the index.
        Primary user would be Storage classes, e.g. CSV and JSON
        :return: component_stock_objects
        """
        return self.component_stock_objects
