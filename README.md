simpleScreenScraper helps automation of information extraction from web pages. 

It takes as an input, a csv file with the following columns (no headers row)
 - URL: this is the url for the page you want to extract information from
 - XPATH: the xpath for the web element you want to extract information from
 - Attribute: attribute of the element you are looking for. 
A sample input file is included in this repo 


An output file is generated with the same data as the input plus on additional column named 'extracted' 


Setup:
In order to get things setup for this script, make sure that the ChromeDriver file (https://sites.google.com/a/chromium.org/chromedriver/downloads) is in the python path in your environment. It should also be given execute permissions

Additionally install the following modules that will be imported by the script

 - selenium
 - pandas
 - csv
