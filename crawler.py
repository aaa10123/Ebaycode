import webbrowser
import pandas as pd
import urllib
from urllib import request
from time import sleep
import selenium
from selenium import webdriver
import numpy as np

def prodcut_search():
    product_name = input('search value: ')
    lobby = input('(1)full crawl'
                  '(2) semi crawl\n')

    bike24 = webbrowser.open('https://www.bike24.com/search?searchTerm=' + product_name)
    bikediscount = webbrowser.open('https://www.bike-discount.de/de/search?sSearch=' + product_name)
    bikecomponents = webbrowser.open('https://www.bike-components.de/en/s/?keywords=' + product_name)
    hibike = webbrowser.open('https://www.hibike.de/finde-produkte-marken-und-mehr-mg-1--1?query=' + product_name)
    r2bikes = webbrowser.open('https://r2-bike.com/navi.php?qs=' + product_name + '&search=')
    xxcycles = webbrowser.open(
        'https://www.xxcycle.com/php/boutique/page.php?nom=RAYON&from=moteurDeRecherche&optionRecherche=&onlySearch=auMieux&catSearch=&marqueSearch=&txtSearch=' + product_name)
    lordgun = webbrowser.open('https://www.lordgunbicycles.co.uk/search?s=' + product_name)
    rosebikes = webbrowser.open('https://www.rosebikes.com/search?q=' + product_name)
    if lobby == '1':
        grizzlycycles = webbrowser.open('https://www.grizzlycycles661.com/search/' + product_name)
        universalcycles = webbrowser.open('https://www.universalcycles.com/search.php?q=' + product_name)
        fanatikbike = webbrowser.open('https://www.fanatikbike.com/pages/search-results-page?q=' + product_name)
        starbike = webbrowser.open('https://www.starbike.com/en/search/?q=' + product_name)
        sevenhundred = webbrowser.open('https://www.7hundred.co.uk/facetresults.aspx?Term=' + product_name)
        alltricks = webbrowser.open('https://www.alltricks.com/Buy/' + product_name)
        actionsports = webbrowser.open('https://www.actionsports.de/en/search?sSearch=' + product_name)
        sigmasports = webbrowser.open('https://www.sigmasports.com/search?query=' + product_name)
        sport4it = webbrowser.open('https://www.sport4it.com/en/search/' + product_name)
        rei = webbrowser.open('https://www.rei.com/search?q=' + product_name)
        sjscycles = webbrowser.open('www.sjscycles.co.uk/search/?term=' + product_name)
        nashbar = webbrowser.open('https://www.nashbar.com/search?s=' + product_name)
        slanecycles = webbrowser.open('https://www.slanecycles.com/extended_search_result.html?keyword=' + product_name)
        hargrovescycles = webbrowser.open('https://www.hargrovescycles.co.uk/facetresults.aspx?term=' + product_name)
        beastybike = webbrowser.open('https://www.beastybike.co.uk/#/dffullscreen/query=' + product_name)
        tritoncycles = webbrowser.open('https://www.tritoncycles.co.uk/search/' + product_name)
        all4cycling = webbrowser.open('https://www.all4cycling.com/en/search?type=product&options%5Bprefix%5D=none&q=fdgdfgf' + product_name)
        merlincycles = webbrowser.open('https://www.merlincycles.com/en-us/search?w=' + product_name)
        gambacicli = webbrowser.open('https://www.gambacicli.com/it/catalogsearch/result/?q=' + product_name)
        probikekit = webbrowser.open('https://www.probikekit.com/elysium.search?search=' + product_name)
        hollandbikeshop = webbrowser.open('https://hollandbikeshop.com/en-gb/advanced_search_result.php?keywords=' + product_name)
        competitivecyclist = webbrowser.open('https://www.competitivecyclist.com/Store/catalog/search.jsp?s=u&q=' + product_name)
        wiggle = webbrowser.open('https://www.wiggle.com/?s=' + product_name)
        bikeman = webbrowser.open('https://www.bikeman.com/search.html?Search=' + product_name)
        bicyclebuys = webbrowser.open('https://www.bicyclebuys.com/searchPage?q=' + product_name)
        bikebug = webbrowser.open('https://www.bikebug.com/?query=' + product_name)
        cyclefastusa = webbrowser.open('https://www.cyclefastusa.com/searchPage?q=' + product_name)
        condorcycles = webbrowser.open('https://www.condorcycles.com/pages/search-results-page?q=' + product_name)
        raddicts = webbrowser.open('https://raddicts.eu/en/suche?controller=search&orderby=position&orderway=desc&search_query=' + product_name)
        ccache = webbrowser.open('https://ccache.cc/pages/search-results-page?q=' + product_name)
        kidscab = webbrowser.open('https://www.kidscab.be/en/zoeken?controller=search&s=' + product_name)
        worldwidecyclery = webbrowser.open('https://www.worldwidecyclery.com/pages/search-results-page?q=' + product_name)








def dhl_tracking():
    driver = webdriver.Chrome(executable_path=r"C:\Users\Dov Fischman\Desktop\chromedriver.exe")

    df = pd.read_excel(r"C:\Users\Dov Fischman\Desktop\code\new-python\ebay calc\ebay2.xlsx")

    delivered = []
    for val in df['tracking']:
        if type(val) is str:
             URL = ('https://www.ordertracker.com/track/'+val)
             URL1 = URL.replace(" ","")

             driver.get(URL1)
             sleep(30)
             content = driver.page_source
             if 'Your package was delivered' in content:
                 delivered.append(val)
    for val in df['tracking']:
        if val in delivered:
            df['tracking'].mask(df['tracking'] == val, val + ' yes' , inplace = True)

    def highlight_cells(val):
        color = 'green' if 'yes' in str(val) else 'white'
        return f'background-color: {color}'

    df.style.applymap(highlight_cells, subset=['tracking'])\
        .to_excel(r"C:\Users\Dov Fischman\Desktop\code\new-python\ebay calc\ebaytracking.xlsx", index=False)



def lobbycrawl():
    q1 = input('1)crawler\n2)tracking\n')
    if q1 == '1':
        prodcut_search()
    else:
        dhl_tracking()





