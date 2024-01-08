# pip install requests
import requests
from bs4 import BeautifulSoup
from lxml import etree as et
from scrape import scrapesite

def compare_pdts(name):
    print("looking for " + name)
    filename = 'reusablehtmls/search' + name + '.htm'
    name = name.replace(' ', '%20')
    url = "https://shopee.sg/search?keyword=" + name
    print(url)

    # proxy = "http://3749742d425110b8cee122d8ef42463a4024e7e0:js_render=true&wait_for=.shopee-searchbar&premium_proxy=true&proxy_country=sg@proxy.zenrows.com:8001"
    # proxies = {"http": proxy, "https": proxy}
    # response = requests.get(url, proxies=proxies, verify=False)
    # print(response.text)
    
    # with open(filename, 'w') as f:
    #     f.write(response.text)
    #     print('saved as {}'.format(filename))

    # soup = BeautifulSoup(response.text, 'html.parser')
    
    with open('reusablehtmls/index.htm', 'r', encoding="utf8") as f: # for testing
        contents = f.read()
        soup = BeautifulSoup(contents, 'html.parser')

    links = []
    key_links = soup.find_all(href=True, attrs={'data-sqe': 'link'})
    for a in key_links:
        links.append(a['href'].encode("ascii", "ignore").decode())

    print(f'Found {len(key_links)} link(s)')
    # print(links)

    for link in links[19]:
        print("https://shopee.sg" + link)
        with open("links.txt", 'a') as f:
            f.write("https://shopee.sg" + link + '\n')
        scrapesite("https://shopee.sg" + link)

compare_pdts("washing machine")