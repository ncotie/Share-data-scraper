# First testing using selenium instead of BeautifulSoup

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
import time
import datetime

page = "https://www.six-group.com/en/products-services/" \
       "the-swiss-stock-exchange/market-data/shares/share-explorer/share-details.CH0012221716CHF4.html#/"

# Instantiate Options class to allow for headless browser
options = Options()
# options.headless = True
# options.page_load_strategy = 'normal'  # I think this is default, but adding in case
# crap, adding the load strategy made it worse, it found nothing at all!?

# path_geckodriver = 'C:\Program Files\Geckodriver (python selenium)'
# Path above can be added as argument when instantiating the webdriver, but not needed
# as we've added the path to PATH Environment Variable
driver = webdriver.Firefox(options=options)
# driver.implicitly_wait(10)  # not making any difference to getting all tags
# Note can also use with webdriver.Firefox() as driver: then indent the rest, for auto-closing

#try:
driver.get(page)
assert "ABB" in driver.title
    # Note failed assert statement gives AssertionError

    # apparently the separated commands are deprecated
    # driver.switch_to_frame('body')
pair_key_list = []

# Accept cookes with button click without a wait -> Does it work ?
# driver.find_element(By.ID, "onetrust-accept-btn-handler").click()
# OR
# Accept cookies with button click, waiting until it is available to be clicked
WebDriverWait(driver, 10).until(ec.element_to_be_clickable((By.ID, "onetrust-accept-btn-handler"))).click()

# After Cookies clicked, perhaps with delay, content should be available
# Note throws NoSuchElementException if none found

# grab the displayed Date in the security-header-datetime
date_webData = driver.find_element(By.CLASS_NAME, "security-header-datetime").find_element(By.TAG_NAME, "dd")
print(date_webData.text)
print(datetime.datetime.strptime(date_webData.text[:10], '%d.%m.%Y'))
# both the above work, the only question is whether I really need to convert to datetime object or not
# there's really no particular need, it would be stored in the same format
# CRAP, problem - if market is open, then you get a date a time like 02.11.2021 / 14:47:31
# and "ValueError: unconverted data remains:  / 14:47:31"
# strptime() has nothing for this, apparently, so I just need to slice the first 10 chars and dump the rest
# OR I could catch the ValueError, check if for unconverted data, then return a warning that the Market is Open.
# OR simpler, just code a check for length of text, if > 10 then market is Open
# Should I include a method parameter whether to fetch data even if market open ?
# CAREFUL: THE MARKET INDEX PAGE INCLUDES A TIME ALSO WHEN MARKET CLOSED !!!!

# just to get the data-pair-key list
pair_key_list = driver.find_elements(By.CLASS_NAME, "data-pair-key")
print(pair_key_list)
for web_element in pair_key_list:
    print(web_element.text)
# now to extend the above to get both keys and values.
# Or rather, I need to restructure the basic type of search above to divide into "News & Data/Key Data"
# and "News & Data/Performance" groups.
# I know this is "News & Data" so I don't actually need to absorb that.
# In both Tabs, I'm in fact only wanting the FIRST TWO data-pair-list tags, the rest are not being stored
print("now trying paired key:value scrape")
radio_tabs_content_tag = driver.find_element(By.CLASS_NAME, "radio-tabs-content")
data_pair_list_tags = radio_tabs_content_tag.find_elements(By.CLASS_NAME, "data-pair-list")
list_data_dicts = []
for data_list in data_pair_list_tags:
    for i in (0, 1):
        data_pair_keys = data_pair_list_tags[i].find_elements(By.CLASS_NAME, "data-pair-key")
        data_pair_values = data_pair_list_tags[i].find_elements(By.CLASS_NAME, "data-pair-value")
        data_dict = {data_pair_keys[j].text: data_pair_values[j].text for j in range(len(data_pair_values))}
        list_data_dicts.append(data_dict)

print(list_data_dicts)
print(list_data_dicts[0])
print(list_data_dicts[1])
# Good the above two dicts are what we need from the News&Data / KeyData and / Performance, perfect.
# This should be repeated after the tab switch



# Now switch to radio tab "Share Details"
# need to click on the right tag, but unfortunately the name of the tab (Share Details)
# is not in the same tag, rather the line above (outside).  Not sure how to first search
# for it, and THEN select the following (inside/child) tag, so instead,
# I'll hard code it to value="$(element.name)2" which is current location of this tab.
# then later code in a check for the string being in the URL as it appends to it.

# note: AND's in CSS selectors need to be chained [][] without spaces.
# ORs, need to repeat whole expression with commas
#WebDriverWait(driver, 10).until(
#    ec.element_to_be_clickable((By.CSS_SELECTOR, "input[type='radio']"
#                                                 "[name='routing']"
#                                                 "[readonly='']"
#                                                 "[value='$(element.name)2)']")))\
#    .click()

# Problem:  the above does NOT manage to click the radio tab at all.  Last time it even managed to disrupt
# the first part from giving output, not sure why ??
# Is there a conflict between the two WebDriverWait's ????
# yes, it's probably clicking TOO FAST ?   Forget the wait totally for now.  Instead python sleep.

time.sleep(3)

#radio_list = []
#radio_list = driver.find_elements(By.CSS_SELECTOR, "input[type='radio']")
#print(radio_list)
#for web_element in radio_list:
#    print(web_element.get_attribute("value"))
# so the above gives $(element.name)0 through 5, which is correct, and it's then only used where I expect it

# test selecting the id="tab-share-details" label tag, and check if we can isolate the input tag below it
# by creating a List and looking for multiple, also checking if more than one by accident
sh_det_list = []
sh_det_list = driver.find_elements(By.ID, "tab-share-details")
for web_element in sh_det_list:
    # for each found tag "tab-share-details", check for tag "Input" below it
    print(web_element.find_element(By.TAG_NAME, "input").get_attribute("value"))
# should only return one, "$(element.name)2"
# good, it did.
# so what's above was really only a test, not needed for final code

# so now make sure a click to that tab works
# no, not directly, gave error "could not be scrolled into view".  Suppose that means I need a scroll down by code
# try the move_to_element() method
share_details_tab = driver.find_element(By.ID, "tab-share-details").find_element(By.TAG_NAME, "input")
ActionChains(driver).move_to_element(share_details_tab).click().perform()
# share_details_tab.click()
# no, it didn't work either, same error.  Ah, seems you need to add .perform() after setting up the ActionChains
# click() can be included in the ActionChains
# WORKS!

# confirm same reading method as previous tab works
# ! No, something wrong, it comes up empty !  Is that because the driver is still seeing the content of the first page?
# Do I need to refresh the driver or something ??
# or perhaps it's just too fast, that it hasn't loaded.  Add a python sleep. <- Yes, that fixed it.
# but really I should do a selenium wait instead to allow for slower network.
# I guess it's because the driver doesn't realize that a javascript change is happening ?
# let me instead of a timer, confirm that that first data-pair-key underneath h3 tag with "Key Data"
# is now changed to Valor symbol ?  The problem with this is that it's hard-coding structure.
# so maybe just a sleep is fine in fact.......  It's more robust
time.sleep(4)
pair_key_list_sh_det = driver.find_elements(By.CLASS_NAME, "data-pair-key")
print(pair_key_list_sh_det)
for web_element in pair_key_list_sh_det:
    print(web_element.text)

print("now trying paired key:value scrape on Share Details tab")
radio_tabs_content_tag_2 = driver.find_element(By.CLASS_NAME, "radio-tabs-content")
data_pair_list_tags_2 = radio_tabs_content_tag_2.find_elements(By.CLASS_NAME, "data-pair-list")
list_data_dicts_2 = []
for data_list in data_pair_list_tags_2:
    for i in (0, 1):
        data_pair_keys_2 = data_pair_list_tags_2[i].find_elements(By.CLASS_NAME, "data-pair-key")
        data_pair_values_2 = data_pair_list_tags_2[i].find_elements(By.CLASS_NAME, "data-pair-value")
        data_dict = {data_pair_keys_2[j].text: data_pair_values_2[j].text for j in range(len(data_pair_values_2))}
        list_data_dicts_2.append(data_dict)

print(list_data_dicts_2)
print(list_data_dicts_2[0])
print(list_data_dicts_2[1])


# TO GET THE SIX INDEX COMPONENTS
baseURL = "https://www.six-group.com/en/products-services/the-swiss-stock-exchange/market-data"
indexName = "SMI"  #  this would be given by User in calling main() ?
equityIndicesURL_suffix = "/indices/equity-indices/{}.html".format(indexName.lower())  # need to make lower case

componentRows_tags = []  # only needed to facilitate fetching of correct tags
componentList_tags = []  # This is where we store the tags we want, of the Index Component names and URLs
componentDict = {}
# move to Index page
driver.get(baseURL + equityIndicesURL_suffix)
# Here I've already accepted cookies but would have to do this  now normally

# First expand the Index Components
# note there seem to be 3 "expander-trigger" but the right one is the first one on page
# also, strangely, the following 2 (not the ones we want) are in fact "expander-trigger "
# with extra space at the end.
#time.sleep(5)
driver.find_element(By.CLASS_NAME, "expander-trigger").click()
#WebDriverWait(driver, 10).until(ec.element_to_be_clickable((By.CLASS_NAME, "expander-trigger"))).click()
# The above should have waited for page load and then clicked the Index Components button to open it
# but it gave a timeout, then worked when I waited 5 sec then just clicked it ?  Why?
# I don't know, but I then tried it without any sleep or wait and it was fine, so I'll just leave it like that

# Now fetch the tags we want
# again, there is only one "expander-body" but two later "expander-body " with space at end
# I had to add that first filter to avoid the SMI Top and SMI Bottom performers
componentRows_tags = driver.find_element(By.CLASS_NAME, "expander-body").find_elements(By.CLASS_NAME, "rt-tr-group")

for rowTag in componentRows_tags:
    # print(rowTag.text)  # only to check stock order, can be removed after

    componentList_tags.append(rowTag.find_element(By.TAG_NAME, "a"))
# arrange into dict with Stock name as key
componentDict = {componentList_tags[i].text: componentList_tags[i].get_attribute('href')
                 for i in range(len(componentList_tags))}

print(componentDict)
print(len(componentDict)) # should be 20 for SMI
# Strange !  Although dict are supposed to preserve insertion order, we don't have alphabetical order
# in the componentDict keys ...  which means that they must've been inserted in something other than
# the alphabetical order found on the page.  It shouldn't be from the componentList_tags list because
# lists are also ordered.  Only conclusion is that the first driver.find_elements was finding elements
# in some order other than the sequence on the page ?!?
# OK->>  It's that the find for "rt-tr-group" is ALSO collecting the SMI Top and SMI Bottom list higher up,
# that we don't want.

# finally:
    # driver.quit()
