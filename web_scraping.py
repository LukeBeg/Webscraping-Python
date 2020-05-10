"""The code introduces the user to webscraping from a course I took on Udemy by Max Schallwig. I have modified the code
on the basis of my understanding. The Javascript part for dynamic webscraping is a bit tricky. As of May 2020, i get blocked by
a Verizon firewall when trying to access Yahoo with javascript. Hopefully, it will get sorted out."""

import pandas as pd
import requests


# apple from yahoo.finance
url = "https://finance.yahoo.com/quote/MMM?p=MMM&.tsrc=fin-srch"



# request the html code from the website url
response = requests.get(url) # gets the url (in html) and everything inside that page
print(response)
print(response.status_code) # 2xx means success, 3xx redirection, 4xx client error

###
Indicators = {
    "Previous Close",
    "Open",
    "Bid",
    "Ask",
    "Day&#x27;s Range",
    "52 Week Range",
    "Volume",
    "Avg. Volume",
    "Market Cap",
    "Beta",
    "PE Ratio (TTM)",
    "EPS (TTM)",
    "Earnings Date",
    "Forward Dividend & Yield",
    "Ex-Dividend Date",
    "1y Target Est"	}

#print(response.text)

htmlText = response.text # save the html code
#>298.87 - 303.24</td></tr><tr
splitList = htmlText.split("Day&#x27;s Range") # split the text at the value you are looking for
                                            # for dates or anything that re-loads is a problem, there is javascript involved.
                                            #
#print(len(splitList)) # this shows the len of for splitList. print() gives 3 so it means there are three occurrencies of the "prev close" which have been split
splitList = htmlText.split("Day&#x27;s Range")
afterFirstSplit = splitList[1].split("\">")[1]
afterSecondSplit = afterFirstSplit.split("</td>") #  per il day range >298.87 - 303.24</td></tr><tr
dataValue = afterSecondSplit[0]
dataValue


print("Search to Find", splitList[1].split("\">")[2]) # this separates it when it finds ">, so in our case the values of the "prev Close" is at the second split

afterFirstSplit = splitList[1].split("\">")

afterSecondSplit = afterFirstSplit.split("</span></td></tr><tr")

data = afterSecondSplit[0]

#stringExample = "Absgjsddkgs"
#print(stringExample.split("s"))


'''now we try to merge all the data at once, in a table '''
data = {}
Indicators = {
    "Previous Close" : [],
    "Open" : [],
    "Bid" : [],
    "Ask" : [],
    "Day&#x27;s Range" : [],
    "52 Week Range" : [],
    "Volume" : [],
    "Avg. Volume" : [],
    "Market Cap" : [],
    "Beta" : [],
    "PE Ratio (TTM)" : [],
    "EPS (TTM)" : [],
    "Earnings Date" : [],
    "Forward Dividend &amp; Yield" : [],
    "Ex-Dividend Date" : [],
    "1y Target Est" : []}

url = "https://finance.yahoo.com/quote/AAPL?p=AAPL&.tsrc=fin-srch"
response = requests.get(url)
htmlText = response.text
for indicator in Indicators:
    print(indicator)
    splitList = htmlText.split(indicator)
    afterFirstSplit = splitList[1].split("\">")[2]
    afterSecondSplit = afterFirstSplit.split("</span></td>")
    dataValue = afterSecondSplit[0]
    Indicators[indicator].append(dataValue)



###########################################################
########## Wikipedia: Extract more company names ##########
###########################################################
import pandas as pd
import requests
wikiURL = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
wikiResponse = requests.get(wikiURL)
data = {"Company" : []}
data2 = {"Company" : []}
#print(wikiResponse.text.split("component companies")[1].split("0001555280")[0]) # takes everything before that number since it is unique.

wikiFirstParse = wikiResponse.text.split("0001555280")[0]

# if you search for the "Component Stocks" it will appear 3 time (2 real times and one for the hyperlink after the first occurrence)
#print(wikiFirstParse[0:10000])
#S&amp;P 500 component stocks
wikiDataTable = wikiFirstParse.split("component stocks")[3] # this is with small letter because on wiki it is like that
                                                            # [3] is the 4th component 0,1,2,3,


#print(wikiDataTable.split("href=")[5].split('">')[1].split("</")[0]) # the 5th hyperlink in the table and it takes everything after that
                                                                     # then you subset by taking everything after "> and then once again by
                                                                     # taking everything before </
hyperLinkSplitWiki = wikiDataTable.split("href=")
start = 4
tracker = 0


# author version
for position in range(len(hyperLinkSplitWiki)): # from zero to len()
    if position > start:
       if "nyse" in hyperLinkSplitWiki[position]:
           if "quote" in hyperLinkSplitWiki[position]:
               tempData = hyperLinkSplitWiki[position].split('">')[1].split("</")[0]
               data["Company"].append(tempData)
       elif "nasdaq" in hyperLinkSplitWiki[position]:
           if "symbol" in hyperLinkSplitWiki[position]:
               tempData = hyperLinkSplitWiki[position].split('">')[1].split("</")[0]
               data["Company"].append(tempData)




# my version
for position in range(5,len(hyperLinkSplitWiki)): # from zero to len()
    if "nyse" and "quote" in hyperLinkSplitWiki[position]:
        tempData = hyperLinkSplitWiki[position].split('">')[1].split("</")[0]
        data2["Company"].append(tempData)
    elif "nasdaq" and "symbol" in hyperLinkSplitWiki[position]:
           # print(hyperLinkSplitWiki[position])
           # print() # this is just for better visualization
        tempData = hyperLinkSplitWiki[position].split('">')[1].split("</")[0]
        data2["Company"].append(tempData)  # there are case where there are more hyperlink like for the location (London, United Kingdom)
            #if len(tempData) > 6:
              #  break



## getting data from YAHOO from all parsed companies


Indicators = {
    "Previous Close" : [],
    "Open" : [],
    "Bid" : [],
    "Ask" : [],
    "Day&#x27;s Range" : [],
    "52 Week Range" : [],
    "Volume" : [],
    "Avg. Volume" : [],
    "Market Cap" : [],
    "Beta" : [],
    "PE Ratio (TTM)" : [],
    "EPS (TTM)" : [],
    "Earnings Date" : [],
    "Forward Dividend &amp; Yield" : [],
    "Ex-Dividend Date" : [],
    "1y Target Est" : []}


#url = "https://finance.yahoo.com/quote/AAPL?p=AAPL&.tsrc=fin-srch"
#response = requests.get(url)
#htmlText = response.text
counter = 0
for ticker in [x for x in data2["Company"] if x != 'BF.B']:  # BF.B exists on yahoo but it is empty so we just remove it
    #print(ticker)
    url = ("https://finance.yahoo.com/quote/"+ticker+"?p="+ticker+"&.tsrc=fin-srch") # the ticker goes between "+ticker+"
    response = requests.get(url)
    htmlText = response.text
    for indicator in [x for x in Indicators if x != ("Day&#x27;s Range") and x != ("52 Week Range") and x != ("Forward Dividend &amp; Yield") and x != ("Earnings Date") and x != ("Ex-Dividend Date")]:
        try:
            splitList = htmlText.split(indicator)
            afterFirstSplit = splitList[1].split("\">")[2]
            afterSecondSplit = afterFirstSplit.split("</span></td>")  # per il day range >298.87 - 303.24</td></tr><tr
            dataValue = afterSecondSplit[0]
            Indicators[indicator].append(dataValue)
        except:
            Indicators[indicator].append("N/A")
    for indicator in [x for x in Indicators if x == ("Day&#x27;s Range") or x == ("52 Week Range") or x == ("Forward Dividend &amp; Yield")]:
        try:
            splitList = htmlText.split(indicator)
            afterFirstSplit = splitList[1].split("\">")[1]
            afterSecondSplit = afterFirstSplit.split("</td>") #  per il day range >298.87 - 303.24</td></tr><tr
            dataValue = afterSecondSplit[0]
            Indicators[indicator].append(dataValue)
        except:
            Indicators[indicator].append("N/A")
    for indicator in [x for x in Indicators if x == ("Earnings Date")]:
        try:
            splitList = htmlText.split(indicator)
            afterFirstSplit = splitList[1].split("\">")
            joined = afterFirstSplit[2] + afterFirstSplit[3]
            afterSecondSplit = joined.split("</span></td></tr><tr")  # per il day range >298.87 - 303.24</td></tr><tr
            dataValue = afterSecondSplit[0]
            dataValue = dataValue.replace('</span><!-- react-text: 78 --> - <!-- /react-text --><span data-reactid="79','-')
            Indicators[indicator].append(dataValue)
        except:
            Indicators[indicator].append("N/A")
    for indicator in [x for x in Indicators if x == "Ex-Dividend Date"]:
        try:
            splitList = htmlText.split(indicator)
            afterFirstSplit = splitList[1].split("\">")[2]
            afterSecondSplit = afterFirstSplit.split("</span></td></tr><tr")
            dataValue = afterSecondSplit[0]
            Indicators[indicator].append(dataValue)
        except:
            Indicators[indicator].append("N/A")

data2.update(Indicators)
final = pd.DataFrame.from_dict(data)



### exercise ###############################################

import requests
import pandas as pd
url2 = "https://webscraper.io/test-sites/tables"
webscraperResponse = requests.get(url2)
webscraper = {"Company" : []}

cells = webscraperResponse.text.split("<td>") # each value is surrounded by <td> </td>
                                             # so basically we are splitting every cell with the "<td>" split

counter = 0
for cell in cells :
    if "Mark" in cell: # the start of the table
        print("Mark", counter)
    if "@twitter" in cell: # end of the table
        print("Twitter", counter)
    counter += 1
    #this tells you the location of the words specified above and you know Mark and @twitter are at the beginning and at the end
    # of the table

# the first table is defined by position 2 and 12

tables = cells[1:21] # from to to 18, but we skip the first

print(tables)
reducedTables = []
for table in tables:
    if "</td>" in table:
        reducedTables.append(table)
print(reducedTables)


doubleReducedTables = []
for table in reducedTables:
    temp = table.split("</td>")[0]
    doubleReducedTables.append(temp)
    #for tableTemp in temp:
        #if "</td>" in tableTemp:
           # doubleReducedTables.append(tableTemp)
print(doubleReducedTables)

webscraper = {"#": [],
              "First Name" : [],
              "Last Name" : [],
              "Username" : []}

for i in range(len(doubleReducedTables)):
    table = doubleReducedTables[i]
    t = i%4
    #value = table.split("</td>")[0]
    if table != "-": # we can take out the empty line
        if t == 0:
            webscraper["#"].append(table)
        elif t == 1 :
            webscraper["First Name"].append(table)
        elif t == 2:
            webscraper["Last Name"].append(table)
        elif t == 3:
            webscraper["Username"].append(table)

df = pd.DataFrame(webscraper)
print(df)


















'''Webscraping with javascript data (dynamic websites)'''
import json
from selenium import webdriver
import pandas as pd
url = "https://finance.yahoo.com/quote/AAPL/key-statistics?p=AAPL"

def fib(n):
    if  n == 0:
        return 0
    elif n ==1:
        return 1
    return fib(n-1) + fib(n-2)

import selenium
from selenium import webdriver

def findJsonPath(jsonObject, target, path, matchType):
    if type(jsonObject) == matchType: # as you go deeper, at a certain point you get keys not json object
        if target in jsonObject:
            return path
        for newKey in jsonObject:
            print(path)
            final = findJsonPath(jsonObject[newKey], target, path + "," + newKey, matchType)
            if final != "":
                return final

    return ""


def FindXPath(element, target, path):
    if target in element.get_attribute("textContent") and element.tag_name == "script":
        return path
    newelements = element.find_elements_by_xpath("./*")
    for newelement in newelements:
        print(path + "/" + newelement.tag_name)
        final = FindXPath(newelement, target, path + "/" + newelement.tag_name)
        if final != "":
            return final
    return ""

options = webdriver.ChromeOptions()
options.add_argument('headless')
driver = webdriver.Chrome(executable_path = "/Users/lucabegatti/Desktop/WebScraping/chromedriver", options = options)
driver.get(url)
element = driver.find_element_by_xpath("html")# takes everything inside below html
print("the final path is the following:",FindXPath(element, "Trailing P/E", "html"))

elements = driver.find_elements_by_xpath("html/body/script")
counter = 1
for element in elements:
    print(element.tag_name)
    if "trailingPE" in element.get_attribute("textContent"):
        print(counter)
        break
    counter +=1
element = driver.find_element_by_xpath("html/body/script[1]")
#print(element.get_attribute("textContent"))
#driver.quit()
tempData = element.get_attribute("textContent").strip("(this));\n")
tempData = tempData.split("root.App.main = ")[1][:-3]
jsonData = json.loads(tempData)
matchType = type(jsonData)
print("Final path is:", findJsonPath(jsonData, "trailingPE", ",", matchType))
#jsonData["html"]
#print(jsonData["context"]["dispatcher"]["stores"]["QuoteSummaryStore"]["summaryDetail"]) # this gives the entire table in a dictionary with all keys
finalData = jsonData["context"]["dispatcher"]["stores"]["QuoteSummaryStore"]["summaryDetail"] # this gives the entire table in a dictionary with all keys which can be easily out into a dataframe
df = pd.DataFrame(finalData)
print(df)

driver.quit()










########### Exercise #######

url = "http://testing-ground.scraping.pro/ajax"
from selenium import webdriver

def FindXPath(element, target, path):
    if target in element.get_attribute("textContent") and element.tag_name == "script":
        return path
    newelements = element.find_elements_by_xpath("./*")
    for newelement in newelements:
        print(path + "/" + newelement.tag_name)
        final = FindXPath(newelement, target, path + "/" + newelement.tag_name)
        if final != "":
            return final
    return ""

options = webdriver.ChromeOptions()
options.add_argument('headless')
driver = webdriver.Chrome(executable_path = "/Users/lucabegatti/Desktop/WebScraping/chromedriver", options = options)
driver.get(url)
#print(driver.page_source)

elements = driver.find_element_by_xpath("html")
finalXPath = FindXPath(elements,"Andrew","html")
print("Final xPath:",finalXPath)

element = driver.find_element_by_xpath(finalXPath)
print("Names:\n",element.text)
driver.quit()
















#########################################################
######## Adding text to a form ##########################

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

url = "https://www.google.com"

browser = webdriver.Chrome(executable_path="/Users/lucabegatti/Desktop/WebScraping/chromedriver")

browser.get(url)

#inputElement = browser.find_element_by_class_name("sbl1")
inputElement = browser.find_element_by_xpath('//*[@id="tsf"]/div[2]/div[1]/div[1]/div/div[2]/input') # right click on the location of the input and copy the xpath
inputElement.send_keys("Yahoo Finance") # this types "Yahoo Finance" on google search
inputElement.submit()

#element = browser.find_element_by_xpath('//*[@id="Rzn5id"]/div/a[2]')
#element.click()
element = WebDriverWait(browser, 10).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="Rzn5id"]/div/a[2]'))).click()
#wait unitil the element is located is loaded or until 10 sec have passed. then it gives an error

ticker = browser.find_element_by_xpath('//*[@id="rso"]/div[1]/div/table/tbody/tr[2]/td[2]/div/span/h3/a')
ticker.click()
policies = WebDriverWait(browser, 10).until(EC.visibility_of_element_located((By.XPATH,'//*[@id="consent-page"]/div/div/div/div[3]/div/form/button[1]'))).click()

browser.quit()

