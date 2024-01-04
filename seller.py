# pip install requests
import requests
from bs4 import BeautifulSoup
from lxml import etree as et


def getsellerdata(url):

    # proxy = "http://2b082df8b4ca3306fc73227e74ccc9d101d7a6a7:js_render=true&wait=10000&premium_proxy=true&proxy_country=sg@proxy.zenrows.com:8001"
    # proxies = {"http": proxy, "https": proxy}
    # response = requests.get(url, proxies=proxies, verify=False)
    # soup = BeautifulSoup(response.text, "html.parser")

    items = []
    with open('test.htm', 'r', encoding="utf8") as f:
        contents = f.read()
        soup = BeautifulSoup(contents, "html.parser")


    dom = et.HTML(str(soup))


    nooflistings = dom.xpath('//*[contains(text(), "shop-page__info")]/div[1]/div[2]/div[1]/div[2]/div[2]/text()')
    print(nooflistings)

    lastactive = dom.xpath('//*[contains(text(), "section-seller-overview-horizontal__active-time")]/text()')
    print(lastactive)

    name = dom.xpath('//*[contains(text(), "section-seller-overview-horizontal__portrait-name")]/text()')
    print(name)

    
    with open('seller.csv', 'w') as f:
        for item in items:
            for i in item:
                f.write(str(i))
                f.write(',')
            f.write('\n')
    return [name, nooflistings, lastactive]
