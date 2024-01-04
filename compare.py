# pip install requests
import requests
from bs4 import BeautifulSoup
from lxml import etree as et

def compare_pdts(name):
    name = name.replace(' ', '%20')
    url = "https://shopee.sg/search?keyword=" + name

    # proxy = "http://7f812834b010ec9b08ca1141ce0f58ca29e80237:js_render=true&wait=10000&premium_proxy=true&proxy_country=sg@proxy.zenrows.com:8001"
    # proxies = {"http": proxy, "https": proxy}
    # response = requests.get(url, proxies=proxies, verify=False)
    # print(response.text)



    links = []
    # f = open('test.txt', 'r')
    # htm = f.read()
    # f.close()
    # print(htm)
    with open('index.htm', 'r', encoding="utf8") as f:

        contents = f.read()
        soup = BeautifulSoup(contents, 'html.parser')

    key_links = soup.find_all(href=True, attrs={'data-sqe': 'link'})
    for a in key_links:
        links.append(a['href'].encode("ascii", "ignore").decode())

    print(f'Found {len(key_links)} link(s)')
    print(links)
    items = []
    #for link in links:
        # url = "https://shopee.sg" + link
        # proxy = "http://2b082df8b4ca3306fc73227e74ccc9d101d7a6a7:js_render=true&wait=10000&premium_proxy=true&proxy_country=sg@proxy.zenrows.com:8001"
        # proxies = {"http": proxy, "https": proxy}
        # response = requests.get(url, proxies=proxies, verify=False)
        # soup = BeautifulSoup(response.text, "html.parser")
    url = 'error'
    with open('test.htm', 'r', encoding="utf8") as f:
        contents = f.read()
        soup = BeautifulSoup(contents, "html.parser")


    dom = et.HTML(str(soup))

    toadd = []
    try:
        price = dom.xpath('//*[contains(text(), "Price Section")]/following-sibling::div/div[last()]/div/text()')[0]
        print(price)
        toadd.append(price)
    except:
        print(url)
        #continue

    try:
        name = dom.xpath('//*[contains(text(), "Product Information Section")]/following-sibling::div/div[1]/span/text()')[0]
        print(name)
    except:
        print(url)
        #continue

    try:
        rating = dom.xpath('//*[contains(text(), "Product Information Section")]/following-sibling::div/div[2]/button[1]/div[1]/text()')[0]
        print(rating)
    except:
        print(url)
        

    try:
        noofratings = dom.xpath('//*[contains(text(), "Product Information Section")]/following-sibling::div/div[2]/button[2]/div[1]/text()')[0]
        print(noofratings)
    except:
        print(url)
        

    try:
        sold = dom.xpath('//*[contains(text(), "Product Information Section")]/following-sibling::div/div[2]/div[1]/div[1]/text()')[0]
        print(sold)
    except:
        print(url)
        

    try:
        imageurl = dom.xpath('//*[contains(text(), "Product Image Section")]/following-sibling::div[1]/div[1]/div[1]/div[2]/picture/img/@src')[0]
        print(imageurl)
    except:
        print(url)
        

    try:
        seller = dom.xpath('//*[contains(text(), "Shop Information Section")]/following-sibling::div[1]/a/@href')[0]
        print(seller)
    except:
        print(url)
        

    #try:
    desc = dom.xpath('//*[contains(text(), "Product Description")]/following-sibling::div[1]/div[1]/p/text()')[0].encode('unicode-escape')

    print(desc)
    #except:
        #print(url)
        

    reviews = []
    for i in range(1,6):
        review = dom.xpath('//*[@class="shopee-product-comment-list"]/div[{}]/div[last()]/div[contains(@style, "position")]/div/text()'.format(i))
        if review == []:
            review = dom.xpath('//*[@class="shopee-product-comment-list"]/div[{}]/div[last()]/div[contains(@style, "position")]/text()'.format(i))

        for t in range(len(review)):
            review[t] = review[t].encode('unicode-escape')
        print(review)
        reviews.append(review)

    print([price, name, rating, noofratings, sold, imageurl, seller, desc, reviews])
    items.append([price, name, rating, noofratings, sold, imageurl, seller, desc, reviews])
    with open('results.csv', 'w') as f:
        for item in items:
            for i in item:
                f.write(str(i))
                f.write(',')
            f.write('\n')

# a = [['a', 'b'], ['c', 3], ['d', 4]]
# with open('results.txt', 'w') as f:
#     for i in a:
#         f.writelines(str(i))