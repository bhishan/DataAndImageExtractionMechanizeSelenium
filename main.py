from selenium import webdriver 
import mechanize
from bs4 import BeautifulSoup
import time
import urllib
import os 
import csv

image_directory = "images"
def main(base_url):
    
    if not os.path.exists(image_directory):
         os.makedirs(image_directory)

    csvwriter = csv.writer(file('scraped.csv', 'wb'))
    csvwriter.writerow(['BARCODE', 'DESCRIPTION', 'PRODUCT NAME', 'IMAGE', 'PRODUCT URL'])

    browser = webdriver.Chrome()

    br = mechanize.Browser()

    br.set_handle_robots(False)

    br.addheaders = [("User-agent","Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.2.13) Gecko/20101206 Ubuntu/10.10 (maverick) Firefox/3.6.13")] 
    
    while True:
        browser.get(base_url)
        time.sleep(10)
        result_elements = browser.find_elements_by_class_name("columnImageTypeB01")
        for each_result in result_elements:
            #product_name = each_result.find_element_by_tag_name("font").text
            
            try:
                product_code_span = each_result.find_element_by_class_name("janCode")
                product_code = product_code_span.get_attribute("content")
            except:
                product_code = ""
                print "product code not available."

            try:
                product_image = each_result.find_element_by_class_name("itemImage")
                image_url = product_image.get_attribute("src")
                download_path = os.path.join(image_directory, product_code + ".jpg")
                urllib.urlretrieve(image_url, image_directory + "/" + product_code+ ".jpg")
                image_path = image_directory + "/" + product_code + ".jpg"
                product_name = product_image.get_attribute("alt")
            except:
                image_url = ""
                image_path = ""
                product_name = ""
                print "image not available for the product."
            
            try:
                product_description = each_result.find_element_by_class_name("multi-line2").text
            except:
                product_description = ""

            try:
                product_link_element = each_result.find_element_by_tag_name("a")
                product_link = product_link_element.get_attribute("href")
                try:
                    product_page = br.open(product_link)
                    soup = BeautifulSoup(product_page)
                    product_details_div = soup.find_all('div', attrs={'class':'unitTypeE01'})
                    
                    product_ingredients_element = product_details_div[1]
                    product_ingredients = product_ingredients_element.find('td').string
                    print product_ingredients
                except:
                    print "inside except product ingredients"
                    product_ingredients = ""
            except:
                print "inside except for product link element"
                product_link = ""

            if product_description:
                product_description = product_description.encode('utf-8')

            if product_name:
                product_name = product_name.encode('utf-8')
            if product_ingredients:
                product_ingredients = product_ingredients.encode('utf-8')
            
            csvwriter.writerow([product_code, product_ingredients, product_name, image_path, product_link])
        try:
            next_element = browser.find_element_by_class_name("next")
            next_link = next_element.find_element_by_tag_name("a")
            base_url = next_link.get_attribute("href")
        except:
            break
        
    #except:
       # print "no results for this keyword."
    

        

if __name__ == '__main__':
    main("http://www.soukai.com/G982/li.html")


