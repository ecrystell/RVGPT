# pip install requests
import requests
from bs4 import BeautifulSoup
from lxml import etree as et
from seller import getsellerdata
from reviews import getreviews, remove_emojis

## HOW TO USE
# 1. get url user is on currently
# 2. scrapesite( urlUserIsOnCurrently, fromUser=True) fromUser prevents compare_pdts loop
# 3. read below for what functions do, scrapesite is below compare_pdts




# Function for comparing similar products
def compare_pdts(name): # Takes in argument of product name
    print("looking for " + name)
    filename = 'reusablehtmls/search' + name + '.htm'
    name = name.replace(' ', '%20') 
    url = "https://shopee.sg/search?keyword=" + name # Replace spaces in name with %20 to search
    print(url)

    ### Scraping the results of search for links
    # proxy = "http://3749742d425110b8cee122d8ef42463a4024e7e0:js_render=true&wait_for=.shopee-searchbar&premium_proxy=true&proxy_country=sg@proxy.zenrows.com:8001"
    # proxies = {"http": proxy, "https": proxy}
    # response = requests.get(url, proxies=proxies, verify=False)
    # print(response.text)
    

    # with open(filename, 'w') as f: # Saving scraped html from proxy to reuse
    #     f.write(response.text)
    #     print('saved as {}'.format(filename))

    # soup = BeautifulSoup(response.text, 'html.parser')
    
    with open('reusablehtmls/index.htm', 'r', encoding="utf8") as f: # for testing, uses existing file
        contents = f.read()
        soup = BeautifulSoup(contents, 'html.parser')

    links = [] # list of 20 links in the first page of results
    key_links = soup.find_all(href=True, attrs={'data-sqe': 'link'})
    for a in key_links:
        links.append(a['href'].encode("ascii", "ignore").decode())

    print(f'Found {len(key_links)} link(s)')
    # print(links)

    for link in links[19]:
        print("https://shopee.sg" + link)
        with open("links.txt", 'a') as f:
            f.write("https://shopee.sg" + link + '\n') # saving link in txt file for debugging

        scrapesite("https://shopee.sg" + link, False) # scraping link, False is show that is not directly from user but from comparing



def scrapesite(url, fromUser): 

    # scraping url using proxy
    proxy = "http://bb51a0e5851590d27c755b2ff8271f2f5fcea393:js_render=true&wait_for=.shopee-searchbar&premium_proxy=true&proxy_country=sg@proxy.zenrows.com:8001"
    proxies = {"http": proxy, "https": proxy}
    response = requests.get(url, proxies=proxies, verify=False)
    soup = BeautifulSoup(response.text, "html.parser")
    
    # with open('test.htm', 'r', encoding="utf8") as f:
    #     contents = f.read()
    #     soup = BeautifulSoup(contents, "html.parser")

    # selected html tag using etree library
    dom = et.HTML(str(soup))

    # navigate to name of product using xpath in etree
    name = dom.xpath('//*[contains(text(), "Product Information Section")]/following-sibling::div/div[1]/span/text()')[0]
    print(name)

    # saving html from url to reuse
    try:
        check = name.replace('/', '')
        filename = 'reusablehtmls/' + check + '.htm'
        with open(filename, 'w') as f:
            f.write(remove_emojis(response.text))
            print("saved as {}".filename)
    except:
        pass

    try:
        # getting seller by navigating using xpath
        seller = dom.xpath('//*[contains(text(), "Shop Information Section")]/following-sibling::div[1]/a/@href')[0]
        seller = "https://shopee.sg" + seller
        getsellerdata(seller) # scraping seller page through url
        print(seller)
    except:
        print("seller " + url)
        
    getreviews(url) # getting reviews through shopee api
    if fromUser: # if scraping the page user is on, activate compare_pdts (to prevent compare_pdts loop)
        compare_pdts(name)

scrapesite('https://shopee.sg/XEXYMIX-XA1131N-Sparky-Crop-Top-Women-T-shirt-Sport-(-10-Colors-)-i.199276028.20445519440?sp_atk=ed075246-1ec5-45b0-913c-7cd027446503&xptdk=ed075246-1ec5-45b0-913c-7cd027446503', True)