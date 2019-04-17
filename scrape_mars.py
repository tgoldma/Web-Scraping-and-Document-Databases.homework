# Dependencies
import time
import re
from bs4 import BeautifulSoup
from splinter import Browser
import pandas as pd
import requests
from selenium import webdriver
import pymongo
from sys import platform

mars_scrape = {}

def initBrowser():
    executable_path = {"executable_path": "chromedriver"}
    return Browser("chrome", **executable_path, headless=True)


def mars_news(browser):
    #Scrape the NASA Mars News Site and collect News Title and Paragraph Text.
    url = 'http://mars.nasa.gov/news/'
    browser.visit(url)
    #Create headline variable 
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    headline = soup.find('div', class_='list_text')
    #Create variables for the title and paragraph in the headline
    title = headline.find('div', class_='content_title').text
    paragraph = headline.find('div', class_='article_teaser_body').text
    return (title, paragraph)



def featured_image(browser):
    #Find the current featured Mars image and scrape
    url_2 = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url_2)
    #Complete button click to image using splinter
    browser.find_by_id('full_image').click()
    browser.is_element_present_by_text('more info', wait_time=5)
    partial_url = "https//www.jpl.nasa.gov"
    #Get partial link for image using splinter
    browser.find_link_by_partial_text('more info').click()
    #Use BeautifulSoup to scrape the featured image
    html = browser.html
    soup_1 = BeautifulSoup(html, 'html.parser')
    time.sleep(5)
    featured_image_url = soup_1.find('figure', class_='lede').find('img')['src']
    print (featured_image_url)
    return(partial_url + featured_image_url)
    

def mars_weather(browser):
    #Visit Mars Weather Twitter and scrape latest weather tweet
    url_3 = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url_3)
    #Use Beautiful Soup to scrape the tweet
    html = browser.html
    soup_2 = BeautifulSoup(html, 'html.parser')
    mars_weather = soup_2.find('p', class_='TweetTextSize TweetTextSize--normal js-tweet-text tweet-text').text
    return(mars_weather)

def mars_facts(browser):
    #Visit Mars Facts webpage and use PANDAS to scrape the table containing Mars Facts
    url_4 = 'https://space-facts.com/mars/'
    #Use Pandas to read in the table
    mars_table = pd.read_html(url_4)
    #Create a dataframe for the table
    df = mars_table[0]
    df.columns = ['Mars Planet Attribute', 'Attribute Value']
    #Set the index for the table to the attribute
    df.set_index('Mars Planet Attribute', inplace=True)
    #Convert to html
    html_table = df.to_html()
    return (html_table)

def mars_hemispheres(browser):
    #Visit USGS Astogeology site to obtain high resolution images for each Mars Hemisphere
    url_5 = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url_5)
    #User splinter to find the images
    browser.html
    test = browser.find_by_css('div.description')
    #Loop through images and titles
    hemi_list = []
    for i in range(len(test)):
        dict1 = {}
        browser.find_by_css('div.description')[i].find_by_css('h3').click()
        sample = browser.find_link_by_text('Sample').first
        dict1['image_url'] = sample['href']                                        
        text = browser.find_by_css('h2.title').text
        dict1['title'] = text
        hemi_list.append(dict1)
        browser.back()
    return(hemi_list)

def scrape():
    
    browser = initBrowser()
    mars_scrape = {}

    mars_news_stuff = mars_news(browser)
    
    mars_scrape['Title']=mars_news_stuff[0]
    mars_scrape['Paragraph']=mars_news_stuff[1]
    
    mars_scrape['partial_url']=featured_image(browser)
    
    mars_scrape['Mars_weather']=mars_weather(browser)
  
    mars_scrape['html_table']=mars_facts(browser)
    
    mars_scrape['Hemi_list']=mars_hemispheres(browser)
    
    browser.quit()

    return(mars_scrape)