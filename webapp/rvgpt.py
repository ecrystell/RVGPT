
# get url of chrome page 
from pywinauto import Application
app = Application(backend='uia')
app.connect(title_re=".*Chrome.*")
element_name="Address and search bar"
dlg = app.top_window()
url = dlg.child_window(title=element_name, control_type="Edit").get_value()
url = 'https://' + url 
print(url)

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

def getreviews(url): 

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

def getsellerdata(url): 

    proxy = "http://7748d960dd1d5d0a6d83cbd2a1595db91b416e72:js_render=true&wait_for=img&premium_proxy=true&proxy_country=sg@proxy.zenrows.com:8001"
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
    proxy = "http://7748d960dd1d5d0a6d83cbd2a1595db91b416e72:js_render=true&wait_for=.shopee-searchbar&premium_proxy=true&proxy_country=sg@proxy.zenrows.com:8001"
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
        
# scrapped = scrapesite(url,True)

# print(scrapped)
    
# # check for fake reviews -- output actual one (nicholas)
import csv

def pretrain(filename):

  import pandas as pd
  import numpy as np
  from nltk.tokenize import RegexpTokenizer
  from collections import OrderedDict

  from torch import nn
  from transformers import Trainer

  import joblib

  import nltk
  from sklearn.feature_extraction.text import TfidfVectorizer
  from sklearn.linear_model import LogisticRegression,SGDClassifier
  from sklearn.metrics import classification_report, confusion_matrix, accuracy_score, recall_score, precision_score, f1_score, pairwise_distances
  from sklearn.model_selection import train_test_split

#   df = pd.read_csv("false_data.csv") # dataset

  test = pd.read_csv(filename, encoding='ISO-8859-1')
  test['comment'] = test.apply(lambda row: str(row['comment']).lower(), axis=1)
  # Preprocessing
  # Remove Punctuations
  tokenizer = RegexpTokenizer(r'\w+')
  test['comment'] = test['comment'].apply(lambda x: ' '.join(word for word in tokenizer.tokenize(x)))
  # Feature Engineering
  test['review_length'] = test['comment'].apply(lambda x: len(x.split()))

  # Convert UNIX timestamp to date and time
  test['date'] = pd.to_datetime(test['ctime'],unit='s').dt.date
  test['time'] = pd.to_datetime(test['ctime'],unit='s').dt.time

  # Maximum Number of Reviews per day per reviewer
  mnr_df1 = test[['userid', 'date']].copy()
  mnr_df2 = mnr_df1.groupby(by=['date', 'userid']).size().reset_index(name='mnr')
  mnr_df2['mnr'] = mnr_df2['mnr'] / mnr_df2['mnr'].max()
  test = test.merge(mnr_df2, on=['userid', 'date'], how='inner')
  # Cosine Similarity
  review_data = test
  res = OrderedDict()

  # Iterate over data and create groups of reviewers
  for row in review_data.iterrows():
      if row[1].userid in res:
          res[row[1].userid].append(row[1].comment)
      else:
          res[row[1].userid] = [row[1].comment]

  individual_reviewer = [{'userid': k, 'comment': v} for k, v in res.items()]
  df2 = dict()
  df2['userid'] = pd.Series([])
  df2['Maximum Content Similarity'] = pd.Series([])
  vector = TfidfVectorizer(min_df=0)
  count = -1
  for reviewer_data in individual_reviewer:
      count = count + 1
      try:
          tfidf = vector.fit_transform(reviewer_data['comment'])
      except:
          pass
      cosine = 1 - pairwise_distances(tfidf, metric='cosine')

      np.fill_diagonal(cosine, -np.inf)
      max = cosine.max()

      # To handle reviewier with just one review
      if max == -np.inf:
          max = 0
      df2['userid'][count] = reviewer_data['userid']
      df2['Maximum Content Similarity'][count] = max

  df3 = pd.DataFrame(df2, columns=['userid', 'Maximum Content Similarity'])
  # left outer join on original datamatrix and cosine dataframe
  test = pd.merge(review_data, df3, on="userid", how="left")
#   df.drop(index=np.where(pd.isnull(df))[0], axis=0, inplace=True)

  logreg = joblib.load('ineedhelp.joblib')

  test['fakeornot'] = 'none'

  # Assuming you have already trained a logistic regression model named logreg
  # and you have a test set with features 'review_length', 'mnr', 'Maximum Content Similarity'

  # Make predictions on the test set
  y_pred = logreg.predict(test[['review_length', 'mnr', 'Maximum Content Similarity']])

  # Assign the predicted labels to a new column 'fakeornot' in the test set
  test['fakeornot'] = y_pred

  # Obtain probability estimates for each class
  probabilities = logreg.predict_proba(test[['review_length', 'mnr', 'Maximum Content Similarity']])

  # Extract the probability of the positive class (class 1)
  confidence_level = probabilities[:, 1]

  # Add the confidence level to a new column 'confidence_level' in the test set
  test['confidence level'] = confidence_level

  fake = test.fakeornot.str.count("fake").sum()
  original = test.fakeornot.str.count("original").sum()
  fake_review = test['comment'].loc[(test.fakeornot == 'fake')]

  return (fake,original, fake_review)


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

# seller = scrapped[0]     
# clean(seller)
# print(seller)

def seller_fraud(socialNbFollowers, socialNbFollows, productsListed,  daysSinceLastLogin, seniority):
    rf = joblib.load("random_forest.joblib")
    features = np.array([[socialNbFollowers, socialNbFollows, productsListed,  daysSinceLastLogin, seniority]])
    return rf.predict_proba(features)

