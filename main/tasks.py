from celery import task 
from celery import shared_task 
from main.models import *
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from django.core.mail import send_mail , EmailMessage , send_mass_mail
from django.core import mail




@shared_task 
def Check_Change():
    email_list = []
    try:
        accounts = Account.objects.all()
        def amazon(url):
            driver.get(url)
            try: 
                try:
                    x  = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'priceblock_ourprice')))
                except:
                    x  = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'priceblock_dealprice')))
                x = x.text 
            except NoSuchElementException:
                x = 'Unavailable'
            return x
            

        def flipkart(url):
            driver.get(url)
            try:
                x  = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, '_1vC4OE._3qQ9m1')))
                x = x.text 
            except NoSuchElementException:
                x = 'Unavailable'
            return x
            

        def ebay(url):
            driver.get(url)
            try:
                x  = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR,'.notranslate.u-cb.convPrice.vi-binConvPrc.padT10')))
                x = x.text 
            except NoSuchElementException:
                x = 'Unavailable'
            return x
            
        PATH ="C:\Program Files\chromedriver.exe"
        chrome_options = Options()  
        chrome_options.add_argument("--headless")  
        driver = webdriver.Chrome(chrome_options=chrome_options , executable_path=PATH)
        
        for acc in accounts:
            F = Favourites.objects.filter(account__user = acc.user)
            if F==None:
                driver.quit()
                
            for f in F:
                url = f.link
                if f.website=='amazon':
                    newprice = amazon(url)
                elif f.website=='flipkart':
                    newprice = flipkart(url)
                else:
                    newprice = ebay(url)
                
                newprice = '49990'
                if newprice!=f.price:
                    name = str(f.name)
                    name = name[ : 30] + '\n' + name[30 : ] 
                    n = 'Price for\n' + str(name) + '\nrecently changed!!'
                    email = EmailMessage(
                        'Notification from Site',
                        '{}'.format(n),
                        'site@gmail.com',
                        [acc.user.email],
                    )
                    email_list.append(email)
                    new_not = Notifications.objects.create(account = acc  ,content = n)
                    new_not.save()
                    f.price = newprice
                    f.save()
                print(f.price)
        try:
            connection = mail.get_connection() 
            connection.send_messages(email_list)
        except Exception:
            print(Exception)
        driver.quit()
    except:
        print('something went wrong')


            


