#!/usr/bin/env python
# coding: utf-8

# In[1]:


import os
from time import sleep
from timeit import timeit
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains


# In[2]:


options = Options()
#options.add_argument("--headless")
options.add_experimental_option("prefs", {
    "download.default_directory": r"E:\PDFs",
    "download.prompt_for_download": False,
    "download.directory_upgrade": True,
    "safebrowsing.enabled": False
})

driver = Chrome("chromedriver.exe", options=options)


# In[3]:


driver.get("https://iccb.idtrust.com.br")


# In[4]:


# login
login = driver.find_element_by_xpath('//*[@id="username"]')
password = driver.find_element_by_xpath('//*[@id="password"]')
login.send_keys("43476556816")
password.send_keys("92hs4oxi")
driver.find_element_by_xpath('//*[@id="bt-login"]').click()


# In[5]:


wait = WebDriverWait(driver, 3)


# In[6]:


# Consulta CCB
menu1 = wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div[2]/form/div/ul/li[1]/a/span[2]')))
menu2 = driver.find_element_by_xpath('//*[@id="menuForm:j_idt17"]/ul/li[1]/ul/li[3]/a')

action = ActionChains(driver)
action.move_to_element(menu1).perform()
action.move_to_element(menu2).perform()

menu2.click()


# In[7]:


# Form
# explict wait for datai to be found
datai = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="form:j_idt35_input"]')))
dataf = driver.find_element_by_xpath('//*[@id="form:j_idt37_input"]')
ccb = driver.find_element_by_xpath('//*[@id="form:j_idt41"]')
filterbt = driver.find_element_by_xpath('//*[@id="form:j_idt50"]')


# In[8]:


def run(data,ccb_n):
    # test
    datai = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="form:j_idt35_input"]')))
    dataf = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="form:j_idt37_input"]')))
    ccb = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="form:j_idt41"]')))
    filterbt = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="form:j_idt50"]')))
    
    
    ccb.clear()
    datai.clear()
    dataf.clear()
    datai.send_keys(f'{data} 00:00:00')
    dataf.send_keys(f'{data} 23:59:59')
    ccb.send_keys(ccb_n)
    filterbt.click()
    # explict wait for CCB to be found
    # Download
    sleep(2)
    try:
        pdf = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="form:tableCcbs:0:j_idt82"]')))
        pdf.click()
    except:
        pdf = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="form:tableCcbs:0:j_idt82"]')))
        pdf.click()


# In[9]:


ccbs = None
dates = None
with open("CCBs.txt") as txt:
    ccbs = txt.read().split("\n")
with open("datas.txt") as txt:
    dates = txt.read().split("\n")
len(ccbs) == len(dates)


# In[10]:


total = len(ccbs)
for x, (ccb_n, date) in enumerate(zip(ccbs,dates),1):
    try:
        print(f"{x}/{total} Getting {ccb_n} - {date} ")
        run(date,ccb_n)
    except:
        pass




# In[11]:


driver.quit()


# In[ ]:





# In[ ]:





