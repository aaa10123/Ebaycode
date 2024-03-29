from datetime import date
import xlwings
from currency_converter import CurrencyConverter
from selenium import webdriver
from bs4 import BeautifulSoup
from crawler import lobbycrawl
from oauth2client.service_account import ServiceAccountCredentials
from openpyxl import Workbook, load_workbook
import pandas as pd
import gspread
import git


#! /anaconda3/bin/python

def template_creator():
    q_1 = input('select template\n1)shipping\n2)site offer\n')
    if q_1 == '1':
        tracking_number = input('input tracking number\n')
        tracking_link = 'https://www.dhl.de/en/privatkunden/pakete-empfangen/verfolgen.html?piececode='+tracking_number
        template = f"""Hello,
        Thank you for choosing to shop at "Bike Away"!
        We just wanted to let you know that your order has been shipped:
    
        Tracking number:  {tracking_number}
        Tracking link: {tracking_link}
                  
        If you have any further questions don't hesitate to contact us.
        Also, be sure to check out some of our other items:
        bikingaway.com - same items but 10% cheaper!"""
        print (template)

    item = input('item name\n')
    item_fixed = item.replace(" ","-")

    item_link = 'https://bikingaway.com/product/'+item_fixed
    template2 = f"""Hello,
    I would like to offer you to purchase directly from our s i t e in order to get a 10% discount. 
    The reason I am offering is because ebay fees are super high and we are trying to establish a small online business
    without the ridiculously high fees here on ebay.
    
    We offer secure paypal chekcout, and would love to have you as a customer:
   {item_link}
    
    It is the exact same item, so no worries. Please let us know if you feel comfortable trusting us with our offer.
    Once again, paypal is the payment method. Very safe."""
    print(template2)





def web_scrapper_ebay():
    q1 = input('scraping origin \n(1)Ebay\n(2)Bikingaway\n')

    URL = input('insert URL ')
    #URL2 = input('insert gmail URL')

    driver = webdriver.Chrome(executable_path=r"/home/dov/chromedriver")

    driver.get(URL)
    content = driver.page_source
    soup = BeautifulSoup(content, "html.parser")
    if q1 == '1':
    #extracting data via BS for ebay
        customer_name = soup.find("span", class_="user-name")
        customer_username = soup.find("span", class_="user-id")
        item = soup.find("span", class_="item-title")
        sale_date = soup.find_all("dd")

        return (customer_name.text,customer_username.text,item.text,str(sale_date[4].text))

    if q1 =='2':
        #this includes customer name, country and email
        customer_info = soup.find('div', class_="address")

        # here I appened all strings from element to list
        result = []
        for i in customer_info.strings:
            result.append(i)


        #this inclues product name
        product = soup.find('td', class_='name')

        # I repeat the same process for the product name
        result2 = []
        for i in product.strings:
            result2.append(i)

        #this includes the date of purchase
        date = soup.find('span', class_='description')
        date = str(date.text)
        date = date[:date.find('via')]

        #this includes order number

        order_num = soup.find('h2', class_='woocommerce-order-data__heading')
        order_num = str(order_num.text)
        order_num = order_num[:order_num.find('det')]

        #result 1: name, result 5: country, result 8: email + order num , result2[1]: product name and date
        return (result[1] + ',' + result[5] ,",".join([order_num,result[8]]) , result2[1] , date)


def currency_converter(amount):
    c = CurrencyConverter()
    Eur_to_USD = c.convert(amount,'EUR','USD')
    return Eur_to_USD

def to_google(fees, listing_price,profit , retailer_p):
    #function finds next available row to insert data into
    def next_available_row(worksheet):
        str_list = list(filter(None, worksheet.col_values(1)))
        return str(len(str_list) + 1)
    # define the scope
    scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']

    # add credentials to the account
    creds = ServiceAccountCredentials.from_json_keyfile_name('/home/dov/Downloads/subtle-melody-344121-f93ac53354c1.json', scope)

    # authorize the clientsheet
    client = gspread.authorize(creds)

    # get the instance of the Spreadsheet from dovifish googledrive
    sheet = client.open_by_key('1_EZ7_RDc1Qipy_vDaO4BbHlFMRLhbQJaI2DgZPF2yeE')
    ws = sheet.worksheet('active')
    free_row = (next_available_row(ws))
    ws.update(f'A{free_row}', "")




    #Customer name, username, item and saledate with web_scrapping function
    customer_name,customer_username,product,purchase_date = web_scrapper_ebay()
    ws.update(f'A{free_row}', str(customer_name))
    ws.update(f'B{free_row}', str(customer_username))
    ws.update(f'C{free_row}', str(product))
    ws.update(f'G{free_row}', str(purchase_date))

    # retailer
    retailer_name = input(
        'select retailer:\n1)bike 24\n2)bikecomponents\n3)xxcycles\n4)bikediscount\n5)rosebikes\n6)other\n')
    if retailer_name == str(1):
        ws.update(f'D{free_row}', 'bike24')
    if retailer_name == str(2):
        ws.update(f'D{free_row}', 'bikecomponents')
    if retailer_name == str(3):
        ws.update(f'D{free_row}', 'xxcycles')
    if retailer_name == str(4):
        ws.update(f'D{free_row}', 'bikediscount')
    if retailer_name == str(5):
        ws.update(f'D{free_row}', 'rosebikes')
    if retailer_name == str(6):
        ws.update(f'D{free_row}', input('enter retailer name\n'))

    #order number
    ws.update(f'E{free_row}', input('enter order number\n'))

    #my order date column
    today = date.today()
    d1 = today.strftime("%d.%m.%Y")
    ws.update(f'H{free_row}', str(d1))

    # retailprice+fees cell
    ws.update(f'J{free_row}', round(fees, 2))
    # ebay price cell
    ws.update(f'K{free_row}', round(listing_price, 2))
    # profit cell
    ws.update(f'L{free_row}', round(profit, 2))
    # profit precent cell
    ws.update(f'M{free_row}', round(round(profit / listing_price, 2)))
    # payment method cell
    ws.update(f'N{free_row}', str(retailer_p) + ' Euro')

    #profit-percentage column
    ws.update(f'M{free_row}', round(profit/listing_price,2))

#calculates the actual selling price after eceving the price from function "selling price"
def selling_price_calc(price):
    if price < 300:
        selling_p = round(price / 0.67,2)
        return selling_p
    if 300 <= price < 600:
        selling_p = round(price / 0.7,2)
        return selling_p
    if 600 <= price < 1500:
        selling_p = round(price / 0.72,2)
        return selling_p
    if 1600 <= price:
        selling_p = round(price / 0.75,2)
        return selling_p



def profit():
    # asking whcih calc is relevant
    q_2 = input('How to calculate fees\n1)Ebay\n2)bikeaway\n')
    #simple while loop to accept only valid inputs
    while True:
        q_1 = input('select retailer currency\n1)Euro\n2)USD\n')
        if q_1.lower() not in ('1', '2'):
            print('wrong input')
            continue
        else:
            break
    listing_p = float(input('please input listing price: '))
    # selected currency is EURO
    if q_1.lower() == '1':
        retailer_p = float(input('please enter retailer price: '))
        #converts retailer price in EURO to USD
        retailer_p_usd = currency_converter(retailer_p)



        if q_2 == '1':
            #calcultes all fees: ebay,bank,payoneer etc and profits
            fees = (listing_p * 0.1614) + retailer_p_usd
            # final profit after all fees are deducted
            profit_ebay = round(listing_p - fees, 2)
            return fees, listing_p, profit_ebay, retailer_p
        if q_2 == '2':
            #calculates fees (5% receiving paypal + 3% conversion rate) and profits for bikeaway
            fees_bikeaway = (listing_p * 0.08) + retailer_p_usd
            profit_bikeaway = round(listing_p - fees_bikeaway, 2)
            return fees_bikeaway, listing_p, profit_bikeaway, retailer_p



    #selected currency is USD
    else:
        retailer_price = float(input('please enter retailer price: '))
        if q_2 == '1':
            fees1 = (listing_p * 0.1614) + retailer_price
            profit_2 = round(listing_p - fees1,2)
            return (fees1, listing_p, profit_2, retailer_price)

        if q_2 == '2':
            fees1 = (listing_p * 0.08) + retailer_price
            profit_bikeaway_2 = round(listing_p - fees1, 2)
            return (fees1, listing_p, profit_bikeaway_2, retailer_price)




def selling_price():
    while True:
        #asks for currency of retailer
        currency_type = input('1)Euro\n 2)USD\n 3)BP \n 4)CAD \n 5)AU:\n ')
        if currency_type not in ('1','2','3','4','5'):
            print('wrong input')
            continue
        else:
            break
    #recieves currency and asks for price of item
    if currency_type in ('1','2','3','4','5'):
        #takes as input the item's price
        item_price = float(input('please enter amount: '))

        # GBP is selceted currency
        if currency_type == '3':
            GBP = item_price * 1.23
            round (GBP,2)
            print ('USD: conversion', round(GBP,2))
            return selling_price_calc(GBP)
        # AUD is selceted currency
        if currency_type == '5':
            AUD = item_price * 0.64
            round (AUD,2)
            print('USD conversion:', round(AUD,2))
            return selling_price_calc(AUD)
        # CAD is selected currency
        if currency_type == '4':
            CAD = item_price * 0.72
            round (CAD,2)
            print('USD conversion:', round(CAD,2))
            return selling_price_calc(CAD)
        #USD is selceted Currency
        if currency_type == '2':
            return selling_price_calc(item_price)
        # EUR is selected currency
        else:
            EUR = currency_converter(item_price)
            print('USD conversion:', round(EUR,2))
            return selling_price_calc(EUR)


def lobby():
    while True:
        print('hello')
        q = input('please select operation:\n1)excel\n2)calc\n3)crawler\n4)template\n')
        if q == '1':
            #accepts 4 varaibles: fees, listing price, profit , retailer price
            x,y,z,w = profit()
            #send 4 above varaibles to excel function to write to ebay2.exe
            to_google(x,y,z,w)
            print('you profit is: ' + str(z))
            lobby()
        if q == '2':

            q_lobby = input('\n1)selling price\n2)profit\n')
            if q_lobby == '1':
                print('selling price: ' + str( selling_price()))
                lobby()
            else:
                x, y, z, w = profit()
                print('profit: ' + str(z))
                lobby()
        if q == '3':
            lobbycrawl()
            lobby()
        if q == '4':
            template_creator()




lobby()



