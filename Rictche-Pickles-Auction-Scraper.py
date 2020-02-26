import urllib.request
from selenium import webdriver
import time
import pandas as pd


driver = webdriver.Chrome()

def get_pickles_data(driver):
    #load page
    driver.get('https://www.pickles.com.au/trucks/item/search#!/search-result?q=(And.ProductType.Trucks._.Make.Mack.)')
    time.sleep(2)
    #set to maximum results and reload
    driver.find_element_by_xpath("//select[@ng-model='itemSearchPageSize']/option[text()='120']").click()
    time.sleep(3)
    #find each individual result
    results = driver.find_elements_by_xpath("//*[@class='result-list']//*[contains(@ng-repeat,'resultItem in searchResults')]")
    
    #store data here
    data = []

    # loop over results for details
    for result in results:
        # Get Links
        link = result.find_element_by_tag_name('a')
        product_link = link.get_attribute("href")
        # Get Titles
        title = link.text
        # Get Location
        loc = result.find_element_by_xpath(".//*[@class='d-flex align-items-center product-attributes-item']")
        location = loc.find_element_by_xpath('.//*[@class="text-truncate ng-binding"]').text
        # Body Type
        body = result.find_element_by_xpath(".//*[@ng-if='resultItem.Body']")
        body_type = body.find_element_by_xpath('.//*[@class="text-truncate ng-binding"]').text
        #add the scraped details to the empty array
        data.append({'Title':title,'Location':location,'Type':body_type,'Link':product_link})
    
    # save to pandas dataframe
    df_pickles = pd.DataFrame(data)
    return df_pickles
    # write to csv
    #df_pickles.to_csv('C:\\Users\\BEN\\Desktop\\OldPrograms\\Auction_Listings_Pickles.csv')

def get_ritchie_data(driver):
    driver.get('https://www.rbauction.com/oceania?keywords=mack&region=11754635523')
    time.sleep(10)
    results = driver.find_elements_by_xpath('//main')
    #print(len(results))
     #store data here
    data = []
    
    # loop over results for details
    for result in results:
        #get title and link
        title = result.find_element_by_tag_name('a')
        product_link = title.get_attribute("href")
        title = title.text
        #get Location
        loc = result.find_elements_by_tag_name('a')
        location = loc[1].text
        #split out Body type from title
        if "Tipper" in title:
            body_type = "Tipper Truck"
        elif "Prime Mover" in title:
            body_type = "Prime Mover"
        else:
            body_type = "Other"
        
        #add the scraped details to the empty array
        data.append({'Title':title,'Location':location,'Type':body_type,'Link':product_link})
    # save to pandas dataframe
    df_ritchie = pd.DataFrame(data)
    return df_ritchie
    # write to csv
    #df_ritchie.to_csv('C:\\Users\\BEN\\Desktop\\OldPrograms\\Auction_Listings_Pickles.csv')


ritchie_df = get_ritchie_data(driver) 
pickles_df = get_pickles_data(driver)   
driver.close()

#Write data to excel
#open file with xlswriter
writer = pd.ExcelWriter('C:\\Users\\BEN\\Desktop\\OldPrograms\\Auction_Listings.xlsx', engine='xlsxwriter')
#Data frame dictionary sheet name is key
frames = {'Pickles': pickles_df, 'Ritchie Bros': ritchie_df}
#loop thru frames and put each on a specific sheet
for sheet, frame in  frames.items(): 
    frame.to_excel(writer, sheet_name = sheet)
writer.save()