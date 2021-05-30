from django.shortcuts import render , get_object_or_404 ,redirect ,HttpResponse
from django.contrib import messages
from django.contrib.auth import login, logout,authenticate
from django.contrib.auth.forms import  AuthenticationForm
from django.contrib.auth.models import User
from  django.contrib.auth.decorators import login_required
from .models import *
from .forms import *
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from friendship.models import Friend, Follow, Block , FriendshipRequest 
import json 
import ast 


# Create your views here.
# Every function redirects to the error page if there is any kind of exception







#This function is for authenticating user and logging him in ..
def Home(request):
    if request.user.is_authenticated:
        return redirect('/home-landing/')
    else:
        if request.method=="POST":
            form = AuthenticationForm(request=request, data=request.POST)
            if form.is_valid():
                username = form.cleaned_data.get('username')
                password = form.cleaned_data.get('password')
                user = authenticate(username=username, password=password)
                if user is not None:
                    login(request , user)
                    return redirect('/home-landing/')
                else:
                    messages.add_message(request, messages.ERROR, "Invalid credentials , Enter again", extra_tags="error")
                    return redirect('')
            else:
                messages.add_message(request, messages.ERROR, "Invalid credentials , Enter again", extra_tags="error")
                return redirect(request.path_info)
        else:
            form = AuthenticationForm(None)
            rform = RegistrationForm(None)
            context = {
                'form':form , 
                'rform':rform
            }
            return render(request , 'home.html' , context)


#After logging user in , using this function user will be directed to the home page !!
@login_required(login_url='/')
def Home_Landing(request):
    try:
        a = Account.objects.get(user= request.user)
        N = Notifications.objects.filter(account__user = request.user) # get the notifications of user
        n_count= N.count()
        context = {
            'account':a,
            'N':N , 
            'count':n_count
        }
        return render(request  , 'home-landing.html', context)
    except:
        return redirect('/error_page/')

#This function handles registration
def Register(request):
    if request.method=="POST":
        rform = RegistrationForm(request.POST)
        if rform.is_valid():
            username = rform.cleaned_data['username']
            password = rform.cleaned_data['password']
            first_name = rform.cleaned_data['first_name']
            last_name = rform.cleaned_data['last_name']
            email= rform.cleaned_data['email']
            u = User.objects.create_user(username=username, password = password , first_name= first_name  , last_name=last_name , email = email)
            u.save()
            user = User.objects.get(username=username)
            A = Account.objects.create(user = user , wallet_amount=0)
            A.save()
            messages.add_message(request, messages.SUCCESS, 'Account Registered Successfully', extra_tags="success")
            return redirect('/')
        else:
            return redirect("/")

    else:
        rform = RegistrationForm(None)
        context = {
            'rform':rform
        }
        return render(request , 'register.html' , context)



    
#Function for logging out
@login_required(login_url='/')
def Logout(request):
    logout(request)
    return redirect('/')


# Funtion for scraping the data from Amazon , Flipkart or Ebay.. Takes time.. , speed depends upon Internet connection..
# After scraping  , products will be rendered in the same page with it's Image , Link , Price in Ascending Order(Lowest Price First)
@login_required(login_url='/')
def Search(request):
   
        listmain= []
        List = []
        Dict = dict()
        query =  request.POST.get('query')
        website = request.POST.get('website')
        print(query)
        print(website)

        searchname = query

        # The place we will direct our WebDriver to
        if website=='amazon':
            url = 'https://www.amazon.in/s?k=' + searchname + '&s=price-desc-rank&qid=1600602305&ref=sr_st_price-desc-rank'
        elif website=='flipkart':
            pass
        elif website=='ebay':
            url = 'https://www.ebay.com/sch/i.html?_from=R40&_nkw=' + searchname + '&_sacat=0&LH_ItemCondition=1000&_sop=15'
        else:
            pass

        PATH ="C:\Program Files\chromedriver.exe" 
        # Creating the WebDriver object using the ChromeDriver
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        driver = webdriver.Chrome(chrome_options = chrome_options , executable_path = PATH)

        # Directing the driver to the defined url
        if website=='flipkart':
            pass
        else:
            driver.get(url)
        
        

        if website=='amazon':
            for j in range(3):
                nextlink = WebDriverWait(driver, 100).until(EC.element_to_be_clickable((By.CLASS_NAME, 'a-last')))
                for i in driver.find_elements_by_css_selector('.s-result-item.s-asin.sg-col-0-of-12.sg-col-16-of-20.sg-col.sg-col-12-of-16'):
                    name = i.find_element_by_class_name('a-size-medium').text
                    link  = i.find_element_by_class_name('a-link-normal').get_attribute('href')
                    img =  i.find_element_by_class_name('s-image').get_attribute('src')
                    
                    try:
                        price = i.find_element_by_class_name('a-price').text
                    except NoSuchElementException:
                        price = ""
                    Dict={
                        'img':img , 
                        'name':name  , 
                        'price':price  , 
                        'link':link
                    }
                    listmain.append(Dict)
                    Dict = {}
                    
                nextlink.click()

        elif website=='flipkart':
            for j in range(3):
                url = 'https://www.flipkart.com/search?q=' + searchname + '&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off&sort=price_asc&page=' + str(j)
                driver.get(url)
                for i in driver.find_elements_by_class_name('_1fQZEK'):
                    driver.execute_script("window.scrollTo(0, window.scrollY + 350)")
                    name = i.find_element_by_class_name('_4rR01T').text
                    link = i.get_attribute('href')
                    img  =  i.find_element_by_class_name('_396cs4').get_attribute('src')
                    try:
                        price = i.find_element_by_class_name('_30jeq3').text
                    except:
                        price = ""
                    Dict={
                        'img':img , 
                        'name':name  , 
                        'price':price  , 
                        'link':link
                    }
                    listmain.append(Dict)
                    Dict = {}
        
        else:
            for j in range(3):
                nextlink = WebDriverWait(driver, 100).until(EC.element_to_be_clickable((By.CLASS_NAME, 'pagination__next')))
                for i in driver.find_elements_by_class_name('s-item__wrapper.clearfix'):
                    name = i.find_element_by_class_name('s-item__title').text
                    img = i.find_element_by_class_name('s-item__image-img').get_attribute('src')
                    try:
                        price = i.find_element_by_class_name('s-item__price').text
                    except:
                        price=''
                    link = i.find_element_by_class_name('s-item__link').get_attribute('href')
                    Dict={
                        'img':img , 
                        'name':name  , 
                        'price':price  , 
                        'link':link
                    }
                    listmain.append(Dict)
                    Dict = {}
                nextlink.click()
            

        if website=='amazon':
            listmain.reverse()
        else:
            pass
        context ={
            'list':listmain ,
            'query':searchname , 
            'website': website
        }
        driver.quit()
        print(listmain)
        return render(request , 'home-landing.html' , context)
   


#This function checks if Amount of the products which user has Favourited has changed , If changed , notifications are given to user..





#Funtion for getting wallet of the  user..
@login_required(login_url='/')
def Wallet(request):
    try:
        account = Account.objects.get(user = request.user)
        r = Requests.objects.filter(account = account) # Transaction requests..
        rcount = r.count()
        context = {
            'account':account ,
            'rcount' :rcount
        }
        return render(request , 'wallet.html' , context )
    except:
        return redirect('/error_page/')


#selecting recipient/donor
@login_required(login_url='/')
def Select_Account(request , temp):
    if request.method=="POST":
        if temp=="send":
            username = request.POST['query1']
        else:
            username = request.POST['query2']
        print(username)
        try:
            user = Account.objects.get(user__username=username)
        except:
            user = None
        if user  is not None and Friend.objects.are_friends(request.user, user.user) == True:
            context= {
                'user':user , 
                'type':temp

            }
            return render(request ,'select_account.html' , context)

        else :   
            messages.error(request  , 'account with username is not a friend')
            return redirect('/wallet/')
    else:
        return render(request , 'select_account.html')

#Function for transactions(sending/requesting money)...
@login_required(login_url='/')
def Transactions(request , id , temp , request_id , request_money):
    try:
        if temp=='send':
            if float(request_money)!= 0.00:
                money = float(request_money)
            else:
                money = float(request.POST['money'])

            print(money)
            myacc = Account.objects.get(user = request.user)
            if money > myacc.wallet_amount:
                messages.add_message(request, messages.ERROR, 'You dont have enough money to send , check your balance and repeat process !', extra_tags="error")
                return redirect('/wallet/')
            a = Account.objects.get(id=id)
            a.wallet_amount += money
            myacc.wallet_amount-=money
            a.save()
            myacc.save()
            msg= 'Amount ' + str(money) + 'INR has been sent to ' + str(a.user.username)
            messages.add_message(request, messages.SUCCESS, msg, extra_tags="success")
            print('this is getting printed')
            if int(request_id)!= 0:
                Delete_Request(request , request_id , 1)
            return redirect('/wallet/')
        else:
            money= float(request.POST.get('money' , False))
            From = Account.objects.get(user = request.user)
            To = Account.objects.get(id = id)
            r= Requests.objects.create(account = To , requestedmoney=money ,requester_username=From.user.username , requester_id = From.id )
            r.save()
            msg= 'Amount ' + str(money) + ' has been requested to ' + str(To.user.username)
            messages.add_message(request, messages.SUCCESS, msg, extra_tags="success")
            return redirect('/wallet/')
    except:
        return redirect('error_page')



#Funtion For adding User's Own favourites
def Add_Fav( request, website):
    try:
        List = request.POST.getlist('favourites')
        account = Account.objects.get(user = request.user)
        for i in List:
            i = ast.literal_eval(i) # this method is used to convert string dict into python dict
            for key , value in i.items():
                if key=='img':
                    img=value
                elif key=='name':
                    name=value
                elif key=='price':
                    price = value
                elif key=='link':
                    link = value
                else:
                    pass
            Favourites.objects.create(account = account ,name = name , price = price , img =img , link =link  , website=website)
            print(name + '-' + price + '-' + img  + '-' + link)

        return redirect('/')
    except:
        return redirect('/error_page/')


# For Viewing User's Favourites
@login_required(login_url='/')
def View_Fav(request , temp):
    try:
        if temp=='main':
            pass
        else:
            N = Notifications.objects.filter(account__user = request.user)
            for n in N:
                n.delete()
        account = Account.objects.get(user = request.user)
        F = Favourites.objects.filter(account= account)
        context ={
            'Fav':F
        }
        return render(request , 'favourites.html', context)
    except:
        return redirect('/error_page/')


#Removing a product from his favourites if user wishes to..
@login_required(login_url='/')
def Remove_Fav(request , id ):
    try:
        f = Favourites.objects.get(id =id)
        f.delete()
        return redirect('/view_fav/main/')
    except:
        return redirect('/error_page/')

#VTo iew the User's Transaction requests
@login_required(login_url='/')
def View_Requests(request):
    try:
        List =[]
        account = Account.objects.get(user = request.user)
        R = Requests.objects.filter(account = account)
        context = {
            'requests':R
        }
        return render(request ,'view_requests.html' ,context )
    except:
        return redirect('/error_page/')


#Deleting User's Transaction Requests if User wishes to...
@login_required(login_url='/')
def Delete_Request(request , id , temp):
    try:
        r = Requests.objects.get(id = id )
        r.delete()
        if temp=='0':
            return redirect('/view_requests/')
        else:
            pass
    except:
        return redirect('/error_page/')

def Friends_List(request):
    all_friends = Friend.objects.friends(request.user)
    frcount = FriendshipRequest.objects.filter(to_user=request.user).count()
    context = {
        'frcount':frcount,
        'friends':all_friends
        }
    return render(request , 'friends_list.html' , context )

def Add_Friends(request):
    if request.method=="POST":
        username = request.POST.get('username')
        if Account.objects.filter(user__username=username).exists():
            try:
                other_user = User.objects.get(username=username)
                Friend.objects.add_friend(
                    request.user,                               # The sender
                    other_user)      # This message is optional
                messages.success(request , 'request sent successfully')
            except:
                messages.add_message(request  , messages.ERROR , 'request already made')

        else:
            messages.add_message(request  , messages.ERROR , 'account with username does not exist')
            return redirect('/add_friends/')
    return render(request , 'add_friends.html')

def View_Frequests(request):
    fr = FriendshipRequest.objects.filter(to_user=request.user)
    context = {
        'fr':fr
    }
    return render(request ,'view_frequests.html' ,context)

def A_Or_R(request , temp , from1):
    if temp=='a':
        FriendshipRequest.objects.get(from_user=User.objects.get(username=from1)).accept()
    else:
        f = FriendshipRequest.objects.get(from_user=User.objects.get(username=from1))
        f.delete()

    return redirect('/friends_list/')




#IF any errors/exceptions/unusual requests were to happen, User will be directed to Error Page using this function
def Error_Page(request):
    return render(request , 'error_page.html')