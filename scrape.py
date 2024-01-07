import requests
from seller import getsellerdata
from reviews import getreviews, remove_emojis
from bs4 import BeautifulSoup
from lxml import etree as et







def scrapesite(url):

    proxy = "http://04d0d2763b84918601e2e2307bd760cd93c13210:js_render=true&wait_for=.shopee-searchbar&premium_proxy=true&proxy_country=sg@proxy.zenrows.com:8001"
    proxies = {"http": proxy, "https": proxy}
    response = requests.get(url, proxies=proxies, verify=False)
    soup = BeautifulSoup(response.text, "html.parser")
    
    # with open('test.htm', 'r', encoding="utf8") as f:
    #     contents = f.read()
    #     soup = BeautifulSoup(contents, "html.parser")


    dom = et.HTML(str(soup))
        

    try:
        seller = dom.xpath('//*[contains(text(), "Shop Information Section")]/following-sibling::div[1]/a/@href')[0]
        seller = "https://shopee.sg" + seller
        getsellerdata(seller)
        print(seller)
    except:
        print("seller " + url)
        
    getreviews(url)


