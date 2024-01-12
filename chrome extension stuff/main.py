# to add content into html
# from js import document  # DOM for this popup page

# para = document.createElement("p")
# seller_fraud = 0.4 
# if seller_fraud > 0.5:
#     if seller_fraud > 0.7: 
#         para.innerHTML = "This seller has a very high risk of engaging in fradulent activities"
#         para.style.color = 'red'
#     else: 
#         para.innerHTML = "This seller has a high risk of engaging in fradulent activities"
#         para.style.color = '#EE4D2D'
# else: 
#     if seller_fraud < 0.3: 
#         para.innerHTML = "This seller is likely reliable"
#         para.style.color = 'orange'
#     else: 
#         para.innerHTML = "This seller is very reliable"
#         para.style.color = 'green'

# para.className = "info"
# document.getElementById("content").appendChild(para)

# para = document.createElement("p")
# rating = 3
# para.innerHTML = 'Recalculated review: {}'.format('⋆' * rating)
# para.className = "info"
# document.getElementById("content").appendChild(para)

# para = document.createElement("p")
# urls = 'urls'
# para.innerHTML = "Similar products available: {}".format(urls)
# para.className = "info"
# document.getElementById("content").appendChild(para)

# # scrape data 
# url = input('Insert URL here: ')

# # pip install requests
import requests
from bs4 import BeautifulSoup
from lxml import etree as et

import re
# import json

def remove_emojis(data):
    emoj = re.compile("["
        u"\U00002700-\U000027BF"  # Dingbats
        u"\U0001F600-\U0001F64F"  # Emoticons
        u"\U00002600-\U000026FF"  # Miscellaneous Symbols
        u"\U0001F300-\U0001F5FF"  # Miscellaneous Symbols And Pictographs
        u"\U0001F900-\U0001F9FF"  # Supplemental Symbols and Pictographs
        u"\U0001FA70-\U0001FAFF"  # Symbols and Pictographs Extended-A
        u"\U0001F680-\U0001F6FF"  # Transport and Map Symbols
        u"\ufe0f"
        u"\u25c6"
        u"\u3002"
                      "]+", re.UNICODE)
    return re.sub(emoj, '', data)

def getreviews(url): # print(getreviews(url))

    # request from shopee api for reviews
    r = re.search(r'i\.(\d+)\.(\d+)', url)
    shop_id, item_id = r[1], r[2]
    ratings_url = 'https://shopee.sg/api/v2/item/get_ratings?filter=0&flag=1&itemid={item_id}&limit=1&offset=0&shopid={shop_id}&type=0'


    testing = requests.get(ratings_url.format(shop_id=shop_id, item_id=item_id)).json()
    reallimit = testing['data']['item_rating_summary']["rating_count"][4]

    # check whether there are any reviews
    print(reallimit)
    while reallimit > 0:
        if reallimit > 59: # max number of reviews accessible at once is 59
            limit = 59
            reallimit -= 59
        else:
            limit = reallimit
            reallimit = 0
        realurl = 'https://shopee.sg/api/v2/item/get_ratings?filter=0&flag=1&itemid={item_id}&limit={limit}&offset=0&shopid={shop_id}&type=0'
        data = requests.get(realurl.format(shop_id=shop_id, item_id=item_id, limit=limit)).json()
        # uncomment this to print all data:
        # print(json.dumps(data, indent=4))

        i = 1
        reviews = []
        for i, rating in enumerate(data['data']['ratings'], 1):
            if rating['comment'] != '':
            
                user = rating['author_username']
                userid = rating['userid']
                ctime = rating['ctime']
                star = rating['rating_star']
                item = rating['itemid']
                comment = remove_emojis(rating['comment']).replace('\n', ' ').replace(',', ' ')
                # print('-' * 80)
                reviews.append([item, user, userid, ctime, star, comment])


        # with open('data/reviews.csv', 'a') as f:
        #     for r in reviews:
        #         f.write("{},{},{},{},{},{}\n".format(r[0], r[1], r[2], r[3], r[4], r[5]))
        print("reviews done")
        return reviews
    else:
        print("no reviews")

def getsellerdata(url): # print(getseller(url))


    proxy = "http://bb51a0e5851590d27c755b2ff8271f2f5fcea393:js_render=true&wait_for=img&premium_proxy=true&proxy_country=sg@proxy.zenrows.com:8001"
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


    item = [name, socialNbFollowers,
     socialNbFollows, productsListed, daysSinceLastLogin, seniority]
    print(item)
    return item

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

    reviews = getreviews(url) # getting reviews through shopee api
    if fromUser: # if scraping the page user is on, activate compare_pdts (to prevent compare_pdts loop)
        # products_url = compare_pdts(name)
        pass

    try:
        # getting seller by navigating using xpath
        seller = dom.xpath('//*[contains(text(), "Shop Information Section")]/following-sibling::div[1]/a/@href')[0]
        seller = "https://shopee.sg" + seller
        seller_data = getsellerdata(seller) # scraping seller page through url
        print(seller)
        return [seller_data, reviews] # product url
    except:
        print("seller " + url)
        return [reviews] # product url 
        
results = scrapesite('https://shopee.sg/XEXYMIX-XA1131N-Sparky-Crop-Top-Women-T-shirt-Sport-(-10-Colors-)-i.199276028.20445519440?sp_atk=ed075246-1ec5-45b0-913c-7cd027446503&xptdk=ed075246-1ec5-45b0-913c-7cd027446503',True)

print(results)

# # running the function 
# from js import document  # DOM for this popup page
# para = document.createElement("p")
# para.innerHTML = scrapesite(url, True)
# para.className = "info"
# document.getElementById("content").appendChild(para)

    
# # check for fake reviews -- output actual one (nicholas)


# # check seller profile/reliability (fraud/no -- qian)

from sklearn.ensemble import RandomForestClassifier
import joblib
import numpy as np 

def clean(seller): 
    for i in range(1,4): 
        if 'k' in seller[i]: 
            seller[i] = round(float(seller[i][:-1])*1000)
        else: 
            seller[i] = int(seller[i])
        
    nums = ''
    if 'days' in seller[4] or 'day' in seller[4]: 
        for i in seller[4]: 
            if i.isdigit(): 
                nums += i 
        seller[4] = int(nums)
    else:
        seller[4] = 0 

    nums = ''
    if 'days' in seller[5] or 'day' in seller[5]: 
        for i in seller[5]: 
            if i.isdigit(): 
                nums += i 
        seller[5] = int(nums)
    elif 'months' in seller[5] or 'month' in seller[5]: 
        for i in seller[5]: 
            if i.isdigit(): 
                nums += i 
        seller[5] = int(nums) * 30 
    elif 'years' in seller[5] or 'year' in seller[5]: 
        for i in seller[5]: 
            if i.isdigit(): 
                nums += i 
        seller[5] = int(nums) * 365
    else:
        seller[5] = 0 

seller = results[0]     
clean(seller)
print(seller)

def seller_fraud(socialNbFollowers, socialNbFollows, productsListed,  daysSinceLastLogin, seniority):
    rf = joblib.load("random_forest.joblib")
    features = np.array([[socialNbFollowers, socialNbFollows, productsListed,  daysSinceLastLogin, seniority]])
    return rf.predict_proba(features)

print(seller_fraud(seller[1], seller[2], seller[3], seller[4], seller[5]))

# # compare products 
# #import compare 
# #compare.compare_pdts("nike jordans")