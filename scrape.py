import requests
from seller import getsellerdata
from reviews import getreviews, remove_emojis
# from compare import compare_pdts
from bs4 import BeautifulSoup
from lxml import etree as et



def scrapesite(url):

    proxy = "http://3749742d425110b8cee122d8ef42463a4024e7e0:js_render=true&wait_for=.shopee-searchbar&premium_proxy=true&proxy_country=sg@proxy.zenrows.com:8001"
    proxies = {"http": proxy, "https": proxy}
    response = requests.get(url, proxies=proxies, verify=False)
    soup = BeautifulSoup(response.text, "html.parser")
    
    # with open('test.htm', 'r', encoding="utf8") as f:
    #     contents = f.read()
    #     soup = BeautifulSoup(contents, "html.parser")


    dom = et.HTML(str(soup))

    name = dom.xpath('//*[contains(text(), "Product Information Section")]/following-sibling::div/div[1]/span/text()')[0]
    print(name)

    try:
        check = name.replace('/', '')
        filename = 'reusablehtmls/' + check + '.htm'
        with open(filename, 'w') as f:
            f.write(remove_emojis(response.text))
            print("saved as {}".filename)
    except:
        pass

    try:
        seller = dom.xpath('//*[contains(text(), "Shop Information Section")]/following-sibling::div[1]/a/@href')[0]
        seller = "https://shopee.sg" + seller
        getsellerdata(seller)
        print(seller)
    except:
        print("seller " + url)
        
    getreviews(url)
    #compare_pdts(name)



