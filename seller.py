# pip install requests
import requests
from bs4 import BeautifulSoup
from lxml import etree as et


def getsellerdata(url):



    proxy = "http://04d0d2763b84918601e2e2307bd760cd93c13210:js_render=true&wait_for=img&premium_proxy=true&proxy_country=sg@proxy.zenrows.com:8001"
    proxies = {"http": proxy, "https": proxy}
    response = requests.get(url, proxies=proxies, verify=False)
    soup = BeautifulSoup(response.text, "html.parser")


    
    # with open('sellertest.htm', 'r', encoding="utf8") as f:
    #     contents = f.read()
    #     soup = BeautifulSoup(contents, "html.parser")


    dom = et.HTML(str(soup))


    nooflistings = dom.xpath('//div[contains(@class, "shop-page__info")]/div[1]/div[2]/div[1]/div[2]/div[2]/text()')[0]
    print(nooflistings)

    lastactive = dom.xpath('//div[contains(@class, "section-seller-overview-horizontal__portrait-status")]/div[1]/text()')[0]
    print(lastactive)

    name = dom.xpath('//h1[contains(@class, "section-seller-overview-horizontal__portrait-name")]/text()')[0]
    print(name)

    item = [name, nooflistings, lastactive]
    with open("seller.csv", 'a') as f:

            f.write(name)
            f.write(',')
            f.write(str(nooflistings))
            f.write(',')
            f.write(lastactive)
            f.write('\n')

    return item

#getsellerdata("https://shopee.sg/nendohitch?categoryId=100012&entryPoint=ShopByPDP&itemId=12112315748")