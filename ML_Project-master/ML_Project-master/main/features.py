from chatgpt_wrapper import ChatGPT
from googlesearch import search

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import pyautogui as py
class chatgpt:
    def __init__(self):
        self.bot = ChatGPT()
    def get(self,question):
        response = self.bot.ask(question)
        return (response)
    
class google:
    def search(question):
        l=[]
        for i in search(question, tld="co.in", num=10, stop=10, pause=2):
            l.append(i)
        return l
        
class lap:
    # from AppOpener import open, close
    # def open(application):
    #     open(application,match_closest=True)
    # def close(application):
    #     close(application,match_closest=True)
    def pretab():
        py.keyDown('alt')
        py.keyDown('shift')
        py.keyDown('tab')
        py.keyUp('alt')
        py.keyUp('shift')
        py.keyUp('tab')
    def posttab():
        py.keyDown('alt')
        py.keyDown('tab')
        py.keyUp('alt')
        py.keyUp('tab')
class open:
    def google(searchterm=""):
        browser = webdriver.Chrome()
        browser.get(searchterm)
    def brave(searchterm=""):
        browser = webdriver.brave()
        browser.get(searchterm)