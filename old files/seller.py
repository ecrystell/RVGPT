# pip install requests
import requests
from bs4 import BeautifulSoup
from lxml import etree as et
from reviews import remove_emojis


def getsellerdata(url):


    proxy = "http://3749742d425110b8cee122d8ef42463a4024e7e0:js_render=true&wait_for=img&premium_proxy=true&proxy_country=sg@proxy.zenrows.com:8001"
    proxies = {"http": proxy, "https": proxy}
    response = requests.get(url, proxies=proxies, verify=False)
    soup = BeautifulSoup(response.text, "html.parser")


    
    # with open('testing use/sellertest.htm', 'r', encoding="utf8") as f:
    #     contents = f.read()
    #     soup = BeautifulSoup(contents, "html.parser")


    dom = et.HTML(str(soup))

    name = dom.xpath('//h1[contains(@class, "section-seller-overview-horizontal__portrait-name")]/text()')[0]

    try:
        check = name.replace('/', '')
        filename = 'reusablehtmls/' + check + '.htm'
        with open(filename, 'w') as f:
            f.write(remove_emojis(response.text))
            print('saved as {}'.format(filename))
    except:
        pass

    
    socialNbFollowers = dom.xpath('//div[contains(@class, "shop-page__info")]/div[1]/div[2]/div[2]/div[2]/div[2]/text()')[0]
    print(socialNbFollowers)

    socialNbFollows = dom.xpath('//div[contains(@class, "shop-page__info")]/div[1]/div[2]/div[3]/div[2]/div[2]/text()')[0]
    print(socialNbFollows)

    productsListed = dom.xpath('//div[contains(@class, "shop-page__info")]/div[1]/div[2]/div[1]/div[2]/div[2]/text()')[0]
    print(productsListed)

    seniority = dom.xpath('//div[contains(@class, "shop-page__info")]/div[1]/div[2]/div[6]/div[2]/div[2]/text()')[0]
    print(seniority)

    daysSinceLastLogin = dom.xpath('//div[contains(@class, "section-seller-overview-horizontal__portrait-status")]/div[1]/text()')[0]
    print(daysSinceLastLogin)

    # hasProfilePicture = False
    # try:
    #     pfp = dom.xpath('//div[contains(@class, "shopee-avatar__img")]/@src')[0]
    #     print(pfp)
    #     hasProfilePicture = True
    # except:
    #     pass


    item = [name, socialNbFollowers, socialNbFollows, productsListed, daysSinceLastLogin, seniority]
    towrite = ''
    for i in item:
        towrite += str(i) + ','
    with open("data/seller.csv", 'a') as f:
        f.write(towrite[:-1] + '\n')
            
    return item

#getsellerdata("https://shopee.sg/nendohitch?categoryId=100012&entryPoint=ShopByPDP&itemId=12112315748")