import argparse
import sys
import time
import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas
import csv

def main():

    #instantiate argparse object
    argsParser = argparse.ArgumentParser()

    #add 
    argsParser = defineArgs(argsParser)

    #read arguments from command line
    args = argsParser.parse_args()

    # setting arguments to global variables
    if args.input:
        inputFile = args.input
    else:
        print ('input file with URLs, XPATHs, Web Attributes is required. Pass it using the -i argument')
        sys.exit()
    if args.output:
        outputFile= args.output
    else:
        print ('Output file name is required. Pass it using the -o argument')
        sys.exit()
    if args.delay:
        customDelay = int(args.delay)
    else:
        customDelay = 0
    
    #load input file into dataFrame
    df = pandas.read_csv(inputFile, names=['url','xpath','attribute'])

    #append extractedData column
    df['extracted']=''

    # Initiate webdriver
    driver = selenium.webdriver.Chrome()
    
    #run the scraper. This function also continually writes the output file
    scrapeScreen(df, outputFile, customDelay, driver)
    
def defineArgs(argsParser): 
    # add arguments
    argsParser.add_argument("--input", "-i", help="Required: input csv file with URLs, target XPATHs, attribute to extract")
    argsParser.add_argument("--output", "-o", help="Required: xpath for the element you are looking for")
    argsParser.add_argument("--delay", "-d", help="Optional: time delay after loading page")
    return(argsParser)

def scrapeScreen(df, outputFile, customDelay, driver):

    rowNum = 0
    while rowNum < df.shape[0]:
        # load page
        driver.get(df['url'][rowNum])

        #wait for customDelay seconds
        time.sleep(customDelay)

        #wait up to 10 more seconds looking for target element.
        print(df['url'][rowNum] + ' - ' + df['xpath'][rowNum] + ' - '+ df['attribute'][rowNum])
        try:
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, df['xpath'][rowNum])))

            # look for target element
            targetElement = driver.find_element_by_xpath(df['xpath'][rowNum])

            # extract attribute
            if df['attribute'][rowNum]=='text':
                extractedAttr = targetElement.text
            else:
                extractedAttr = targetElement.get_attribute(df['attribute'][rowNum])

            # update df with extracted attribute
            df['extracted'][rowNum] = extractedAttr

            #update output file
            df.to_csv(outputFile)
   
        # if element is not found:
        except Exception as e:
            # update df with extracted attribute
            df['extracted'][rowNum] = 'Could not find'

            #update output file
            df.to_csv(outputFile)
        
        #increment loop
        rowNum+=1

main()
