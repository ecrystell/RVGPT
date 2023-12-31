# pip install requests
import requests
from bs4 import BeautifulSoup
from lxml import etree as et


# url = "https://shopee.sg/search?keyword=nike%20jordans"
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
#print(links)
items = []
for link in links:
    url = "https://shopee.sg" + link
    proxy = "http://7f812834b010ec9b08ca1141ce0f58ca29e80237:js_render=true&wait=5000&premium_proxy=true&proxy_country=sg@proxy.zenrows.com:8001"
    proxies = {"http": proxy, "https": proxy}
    response = requests.get(url, proxies=proxies, verify=False)
    print(response.text)

    # with open('test.htm', 'r', encoding="utf8") as f:
    #     contents = f.read()
    #     soup = BeautifulSoup(contents, "html.parser")

    soup = BeautifulSoup(response.text, "html.parser")
    dom = et.HTML(str(soup))
   
    price = dom.xpath('//*[contains(text(), "Price Section")]/following-sibling::div/div[last()]/div/text()')[0]
    print(price)

    name = dom.xpath('//*[contains(text(), "Product Information Section")]/following-sibling::div/div[1]/span/text()')[0]
    print(name)

    rating = dom.xpath('//*[contains(text(), "Product Information Section")]/following-sibling::div/div[2]/button[1]/div[1]/text()')[0]
    print(rating)

    noofratings = dom.xpath('//*[contains(text(), "Product Information Section")]/following-sibling::div/div[2]/button[2]/div[1]/text()')[0]
    print(noofratings)

    sold = dom.xpath('//*[contains(text(), "Product Information Section")]/following-sibling::div/div[2]/div[1]/div[1]/text()')[0]
    print(sold)

    imageurl = dom.xpath('//*[contains(text(), "Product Image Section")]/following-sibling::div[1]/div[1]/div[1]/div[2]/picture/img/@src')[0]
    print(imageurl)

    seller = dom.xpath('//*[contains(text(), "Shop Information Section")]/following-sibling::div[1]/a/@href')[0]
    print(seller)

    desc = dom.xpath('//*[contains(text(), "Product Description")]/following-sibling::div[1]/div[1]/p/text()')[0]
    print(desc[:10])

    for i in range(1,6):
        review = dom.xpath('//*[@class="shopee-product-comment-list"]/div[{}]/div[last()]/div[contains(@style, "position")]/div/text()'.format(i))
        if review == []:
            review = dom.xpath('//*[@class="shopee-product-comment-list"]/div[{}]/div[last()]/div[contains(@style, "position")]/text()'.format(i))

        for t in range(len(review)):
            review[t] = review[t].encode('unicode-escape')

        print(review)
    items.append(price, name, rating, noofratings, sold, imageurl, seller, desc, review)