
#%%
#import dependences
from bs4 import BeautifulSoup
from splinter import Browser
import requests
import os
import pandas as pd


#%%
#chromedriver
browser = Browser('chrome', headless=False)


#%%
#Scrape the NASA Mars News Site and collect the latest News Title and Paragraph Text. 

url = 'http://mars.nasa.gov/news/'
browser.visit(url)


#%%
html = browser.html
soup = BeautifulSoup(html, 'html.parser')

headline = soup.find('div', class_='list_text')
print(headline)


#%%
#collect the latest News Title and Paragraph Text.
title = headline.find('div', class_='content_title').text
paragraph = headline.find('div', class_='article_teaser_body').text


#%%
#print the latest News Title and Paragraph Text.
print(title)
print(paragraph)


#%%
#Find Visit the url for JPL Featured Space Image
url_2 = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
browser.visit(url_2)


#%%
#buttonclick
clickbutton = browser.find_by_id('full_image').click()

browser.is_element_present('more info', wait_time=15) # True, using wait_time

#%%
#Use splinter to navigate the site and find the image url for the current 

link_found_splinter = browser.find_link_by_partial_text('more info').click()


#%%
#Use BSoup to scrape image
html = browser.html
soup_1 = BeautifulSoup(html, 'html.parser')

featured_image_url = soup_1.find('figure', class_='lede').a.img
print("https://www.jpl.nasa.gov" + featured_image_url['src'])


#%%
#Visit the Mars Weather twitter account here and scrape the latest Mars weather tweet from the page. 
#Save the tweet text for the weather report as a variable called mars_weather.

url_3 = 'https://twitter.com/marswxreport?lang=en'
browser.visit(url_3)


#%%
#Use BSoup to scrape the tweet
html = browser.html
soup_2 = BeautifulSoup(html, 'html.parser')

mars_weather = soup_2.find('p', class_='TweetTextSize TweetTextSize--normal js-tweet-text tweet-text').text
print(mars_weather)


#%%
#Visit the Mars Facts webpage here and use Pandas to scrape the table containing facts about the planet 
#including Diameter, Mass, etc.
url_4 = 'https://space-facts.com/mars/'


#%%
#use pandas to read in the table
mars_table = pd.read_html(url_4)
mars_table
#Use Pandas to convert the data to a HTML table string


#%%
#Create a dataframe and rename
df = mars_table[0]
df.columns = ['Mars Planet Attribute', 'Attribute Value']
df.head()


#%%
#remove index and make index Mars Planet Attribute
df.set_index('Mars Planet Attribute', inplace=True)
df.head()


#%%
#Convert to html, Use Pandas to convert the data to a HTML table string
html_table = df.to_html()
html_table


#%%
#get rid of new lines
html_table.replace('\n', '')


#%%
#Output table 
df.to_html('table.html')


#%%
#Visit the USGS Astrogeology site here to obtain high resolution images for each of Mar's hemispheres.e
url_5 = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
browser.visit(url_5)


#%%
#User splinter to find the images
html = browser.html
test = browser.find_by_css('div.description')


#%%
#Loop through images and titles
hemi_list = []
for i in range(len(test)):
    dict1 = {}
    browser.find_by_css('div.description')[i].find_by_css('h3').click()
    sample = browser.find_link_by_text('Sample').first
    dict1['image_url'] = sample['href']
    #print(sample['href'])                                           
    text = browser.find_by_css('h2.title').text
    dict1['title'] = text
    hemi_list.append(dict1)
    browser.back()


#%%
#Print
print(hemi_list)


#%%
#Make dictionaries to save all of the scrape data for use in Python scripts
mars_dictionary = {}
mars_dictionary['Headline']=headline
mars_dictionary['Title']=title
mars_dictionary['Featured_Image_url']=f"https//www.jpl.nasa.gov/" + featured_image_url['src']
mars_dictionary['Mars_weather']=mars_weather
mars_dictionary['Mars_table']=mars_table
mars_dictionary['Hemi_list']=hemi_list
print(mars_dictionary)


#%%



