# -*- coding: gbk -*-
"""
Created on Tue Apr 01 11:21:29 2014

@author: tanhe
"""

from selenium import webdriver
import selenium.webdriver.support.ui as ui
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep
from random import choice
import re
#import pickle

browser = webdriver.Chrome() # 打开谷歌浏览器
wait = ui.WebDriverWait(browser,10)

browser.get("http://s.weibo.com/")

def login(username,password):

    wait.until(lambda browser: browser.find_element_by_xpath("//a[@node-type='loginBtn']"))
    browser.find_element_by_xpath("//a[@node-type='loginBtn']").click()
    
    wait.until(lambda browser: browser.find_element_by_xpath("//input[@name='username']"))
    user = browser.find_element_by_xpath("//input[@name='username']")
    user.clear()
    user.send_keys(username)
    psw = browser.find_element_by_xpath("//input[@name='password']")
    psw.clear()
    psw.send_keys(password)
    browser.find_element_by_xpath("//div[6]/a/span").click()

##登陆完成，若出现用户名，则开始进行搜索
def search(searchWord):
    
    wait.until(lambda browser: browser.find_element_by_class_name("gn_name"))
    
    inputBtn = browser.find_element_by_class_name("searchInp_form")
    inputBtn.clear()
    inputBtn.send_keys(searchWord.strip().decode("gbk"))
    #inputBtn.send_keys("小米手机".strip().decode("gbk"))
    browser.find_element_by_class_name('searchBtn').click()
    
    #wait.until(lambda browser: browser.find_element_by_class_name("search_num"))

#texts = browser.find_elements_by_xpath("//dl[@class='feed_list W_linecolor ']/dd[@class='content']/p[@node-type='feed_list_content']/em")
def gettext():
    content =[]
    wait.until(lambda browser: browser.find_element_by_class_name("search_page_M"))
    texts = browser.find_elements_by_xpath("//dl[@action-type='feed_list_item']/dd[@class='content']/p[@node-type='feed_list_content']/em")
    #print len(texts)
    for n in texts:
        try:
            highpoints = re.compile(u'[\U00010000-\U0010ffff]')
        except re.error:
		highpoints = re.compile(u'[\uD800-\uDBFF][\uDC00-\uDFFF]')
        mytext =  highpoints.sub(u'', n.text)
        print mytext.encode("gbk")
        content.append(mytext.encode("utf-8"))
    return content
    
def nextPage():
    #wait.until(lambda browser: browser.find_element_by_class_name("search_page_M"))
    if browser.find_elements_by_xpath("//ul[@class='search_page_M']") != None:
        nums = len(browser.find_elements_by_xpath("//ul[@class='search_page_M']/li"))
        #browser.execute_script("window.scrollTo(0, 7100)")
        pg = browser.find_element_by_xpath("//ul[@class='search_page_M']/li[%d]/a" %nums) #.text.encode("gbk")
        y = pg.location['y']+100
        print y
        browser.execute_script('window.scrollTo(0, {0})'.format(y))        
        ActionChains(browser).move_to_element(pg).click(pg).perform()

def main():
    login()
    search("佟丽娅")
    text =[]
    for i in range(0,10):
        text=text +gettext()
        sleep(choice([1,2,3,4]))
        nextPage()         
    print len(text)
    
main()