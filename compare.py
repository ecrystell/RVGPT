# pip install requests
import requests
from bs4 import BeautifulSoup
from lxml import etree as et
from scrape import scrapesite

def compare_pdts(name):
    print("looking for " + name)
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
    # print(links)

    for link in links[14:]:
        print("https://shopee.sg" + link)
        # with open("links.txt", 'a') as f:
        #     f.write("https://shopee.sg" + link + '\n')
        scrapesite("https://shopee.sg" + link)

compare_pdts("nike jordans")