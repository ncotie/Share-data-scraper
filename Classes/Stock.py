from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import time


class Stock:
    """
    Implements a single stock (share issued by a company) object
    for the purpose of the data scraper.
    A stock is a component of a stockIndex.
    """
    def __init__(self, name, url):
        """
        Constructor for class Stock
        :param url: string of complete market data URL
        :param name: string, identifier of stock
        """
        # Attributes received as constructor arguments
        self.name = name
        self.url = url
        # Initializing data dictionaries to be used later during scraping
        self.news_data_KeyData = {}
        self.news_data_Performance = {}
        self.share_det_KeyData = {}
        self.share_det_Profile = {}
        # Storage of date of data
        self.scraped_date = ""

    def scrape_data(self, driver, open_market_ok):
        """
        Order for a Stock instance to scrape data for itself.
        Scraped data is stored in dictionaries but are not returned, 
        rather a result code is returned as to whether scraping was 
        successful or not.
        Method should be internal to package (protected)
        :param driver: selenium.Webdriver
        :param open_market_ok: Boolean, does operator desire data scraping even if market
        not closed yet.
        :return: result, integer code indicating what sort of result.
        O = successful
        1 = webpage indicates market is still open, while user has specified not scraping data
        while market is open
        :return: date_string, a string of web data's date.  This serves to check if we already
        have this data scraped and stored
        """

        def collect_data_pair_tags(data_pair_list_tags):
            """
            Nested function to assemble the stock data keys and values from the appropriate tags
            and pack into four dictionaries.
            Their types and names are preset by the structure of the web page as currently designed by SIX.
            :param data_pair_list_tags:
            :return:
            """
            list_data_dicts = []
            for i in (0, 1):
                # For each data-pair-list tag, store the two tags we want to scrape, into two temporary lists
                data_pair_keys = data_pair_list_tags[i].find_elements(By.CLASS_NAME, "data-pair-key")
                data_pair_values = data_pair_list_tags[i].find_elements(By.CLASS_NAME, "data-pair-value")
                # Then arrange the aligned values into a temporary dictionary
                data_dict = {data_pair_keys[j].text: data_pair_values[j].text for j in range(len(data_pair_values))}
                # And append this temporary dictionary to our output list
                list_data_dicts.append(data_dict)
            # NOTE: The above two-step loop and storage into the list could be simplified, but is a better
            # setup if this code were to be extended to scrape more than the first two sets of data on this page.
            return list_data_dicts
            # -------- End of nested function ---------- #

        # Open stock's own page
        try:
            driver.get(self.url)
            # Confirm title includes stock name
            assert self.name in driver.title
        except Exception:
            return "Error opening stock webpage or invalid URL.",\
                   ""   # An empty value for scraped_date field

        # Driver was already on market web page, so no cookies need to be accepted at this point.
        # Grab the displayed Date in the security-header-datetime.
        # This will need to be attached to the data and later stored in the output files.

        time.sleep(10)  # to allow for loading time
        try:
            date_string_full = driver.find_element(By.CLASS_NAME, "security-header-datetime")\
                .find_element(By.TAG_NAME, "dd").text
            # Note, the date value is only being taken as a string, same as displayed on the web page
            # and truncated to remove the time, in the case of the market being open still.
            # Dates could be later managed via data pre-processing if necessary.
            self.scraped_date = date_string_full[:10]    # truncate any time value
            if len(date_string_full) > 10:    # If time was also displayed
                # in the case of the SIX pages, time displayed means the market is still open,
                # and data are not finalized for the day.
                if not open_market_ok:
                    return "Market is open. User specified that it is not allowed " \
                           "to scrape data while market is open.", \
                           self.scraped_date

            # Now go ahead for first webpage Tab of data, "News & Data"
            # Web page automatically loads this page on opening page
            # All needed content is under the only "radio-tabs-content" tag,
            # in separate data-pair-list tag sections, of which there are multiple.
            # Here we only want to search the first two data-pair-lists' contents for scraping.
            radio_tabs_content_tag = driver.find_element(By.CLASS_NAME, "radio-tabs-content")
            data_pair_list_tags = radio_tabs_content_tag.find_elements(By.CLASS_NAME, "data-pair-list")

            # Call nested function to collect the data keys and values into a list of dictionaries,
            # one per block of data
            list_data_dicts = collect_data_pair_tags(data_pair_list_tags)

            # Now store the two dicts separately **in Instance Data** and pause
            self.news_data_KeyData = list_data_dicts[0]
            self.news_data_Performance = list_data_dicts[1]
            time.sleep(4)

            # Now switch to the Tab, "Share Details", by clicking on the Tab, rather than reloading the page
            # First have to scroll down to be able to reliably click the Tab, however
            driver.execute_script("window.scrollTo(0,500)")
            share_details_tab = driver.find_element(By.ID, "tab-share-details").find_element(By.TAG_NAME, "input")
            ActionChains(driver).move_to_element(share_details_tab).click().perform()

            # Pause then locate the parent tags on this Tab of data
            # Note: this reuses the same tag storage items as before.
            time.sleep(4)
            radio_tabs_content_tag = driver.find_element(By.CLASS_NAME, "radio-tabs-content")
            data_pair_list_tags = radio_tabs_content_tag.find_elements(By.CLASS_NAME, "data-pair-list")

            # Call nested function again to collect the data keys and values on this Tab,
            # into a list of dictionaries, one per block of data
            list_data_dicts = collect_data_pair_tags(data_pair_list_tags)

            # Now store the two dicts separately **in Instance Data**
            self.share_det_KeyData = list_data_dicts[0]
            self.share_det_Profile = list_data_dicts[1]

            result = 0  # successful
            return result, self.scraped_date
        except Exception:
            return "Problem parsing stock's webpage tags.",\
                   ""    # empty string for scraped_date

    def get_data(self):
        """
        Retrieves the set of data dictionaries housing the scraped data.
        Method should be internal to package (protected)
        :return: List[Map] returns a list of the 4 data dictionaries prefaced by the date and name
        """
        result_list = [self.scraped_date,
                       self.name,
                       self.news_data_KeyData,
                       self.news_data_Performance,
                       self.share_det_KeyData,
                       self.share_det_Profile]
        return result_list

    def get_name(self):
        """
        getter function to fetch name for instance
        :return: name
        """
        return self.name
