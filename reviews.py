       
import re
import json
import requests

# function to remove emojis from text as python cannot decode
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
        print(json.dumps(data, indent=4))

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
        


#getreviews("https://shopee.sg/Nike-Air-Monarch-IV-4-White-Blue-Silver-Daddy-Shoes-Casual-Retro-Time-Men's-ACS-415445-102-i.184639455.19814568437?sp_atk=74a0bddd-967c-43d9-86c1-c83b5d9906cb&xptdk=74a0bddd-967c-43d9-86c1-c83b5d9906cb")
