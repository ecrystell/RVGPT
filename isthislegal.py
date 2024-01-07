import json
import pandas as pd
import requests

limit = 30
match_id = 1075
page_no = 0

def scrapeProduct(limit, match_id, page_no):
    
    df_product = pd.DataFrame()
    df_rating = pd.DataFrame()
    
    url = "https://shopee.co.id/api/v4/search/search_items"
    
    querystring = {"by":"relevancy","limit":limit,"match_id":match_id,"newest":page_no,"order":"desc","scenario":"PAGE_OTHERS","version":"2"}

    payload = ""
    headers = {
        "cookie": "REC_T_ID=3cd4a8c4-b8a0-11eb-ac80-b49691342bf6",
        "authority": "shopee.sg",
        "pragma": "no-cache",
        "cache-control": "no-cache",
        "sec-ch-ua": "^\^"
    }
    
    url = "https://shopee.sg/api/v4/search/search_items"

    response = requests.request("GET", url, data=payload, headers=headers, params=querystring)

    jsondata = json.loads(response.text)
    print(jsondata)

    for product in jsondata['items']:
        #product data
        itemid = product['item_basic']["itemid"]
        shopid = product['item_basic']["shopid"]
        name = product['item_basic']["name"]
        currency = product['item_basic']["currency"]
        stock = product['item_basic']["stock"]
        ctime = product['item_basic']["ctime"]
        historical_sold = product['item_basic']["historical_sold"]
        liked_count = product['item_basic']["liked_count"]
        view_count = product['item_basic']["view_count"]
        catid = product['item_basic']["catid"]
        brand = product['item_basic']["brand"]
        price = product['item_basic']["price"]
        price_min = product['item_basic']["price_min"]
        price_max = product['item_basic']["price_max"]
        price_min_before_discount = product['item_basic']["price_min_before_discount"]
        price_max_before_discount = product['item_basic']["price_max_before_discount"]
        price_before_discount = product['item_basic']["price_before_discount"]
        has_lowest_price_guarantee = product['item_basic']["has_lowest_price_guarantee"]
        raw_discount = product['item_basic']["raw_discount"]
        rating_star = product['item_basic']["item_rating"]["rating_star"]
        show_free_shipping = product['item_basic']["show_free_shipping"]
        is_preferred_plus_seller = product['item_basic']["is_preferred_plus_seller"]
        shop_location = product['item_basic']["shop_location"]
        has_model_with_available_shopee_stock = product['item_basic']["has_model_with_available_shopee_stock"]
        can_use_cod = product['item_basic']["can_use_cod"]
        is_on_flash_sale = product['item_basic']["is_on_flash_sale"]

        prod_row = pd.Series([itemid, shopid, name, currency, stock, ctime, historical_sold, liked_count, view_count, catid, brand, price, price_min, price_max, price_min_before_discount, price_max_before_discount, price_before_discount, has_lowest_price_guarantee, raw_discount, rating_star, show_free_shipping, is_preferred_plus_seller, shop_location, has_model_with_available_shopee_stock, can_use_cod, is_on_flash_sale])
        row_df_prod = pd.DataFrame([prod_row], index = [itemid])
        df_product = pd.concat([df_product, row_df_prod])
        
        #product rating
        rating_total = product['item_basic']["item_rating"]["rating_count"][0]
        rating_count_1 = product['item_basic']["item_rating"]["rating_count"][1]
        rating_count_2 = product['item_basic']["item_rating"]["rating_count"][2]
        rating_count_3 = product['item_basic']["item_rating"]["rating_count"][3]
        rating_count_4 = product['item_basic']["item_rating"]["rating_count"][4]
        rating_count_5 = product['item_basic']["item_rating"]["rating_count"][5]
        
        rating_row = pd.Series([itemid, rating_total, rating_count_1, rating_count_2, rating_count_3, rating_count_4, rating_count_5])
        row_df_rating = pd.DataFrame([rating_row], index = [itemid])
        df_rating = pd.concat([df_rating, row_df_rating])
           
    df_product = df_product.rename(columns={0: "itemid",
                                            1: "shopid", 
                                            2: "name", 
                                            3: "currency", 
                                            4: "stock", 
                                            5: "ctime", 
                                            6: "historical_sold", 
                                            7: "liked_count", 
                                            8: "view_count", 
                                            9: "catid", 
                                            10: "brand", 
                                            11: "price", 
                                            12: "price_min", 
                                            13: "price_max", 
                                            14: "price_min_before_discount", 
                                            15: "price_max_before_discount", 
                                            16: "price_before_discount", 
                                            17: "has_lowest_price_guarantee", 
                                            18: "raw_discount", 
                                            19: "rating_star", 
                                            20: "show_free_shipping", 
                                            21: "is_preferred_plus_seller", 
                                            22: "shop_location", 
                                            23: "has_model_with_available_shopee_stock", 
                                            24: "can_use_cod", 
                                            25: "is_on_flash_sale"}, errors="raise")

    df_rating = df_rating.rename(columns={0: "itemid", 
                                          1: "rating_total", 
                                          2: "rating_count_1", 
                                          3: "rating_count_2",
                                          4: "rating_count_3",
                                          5: "rating_count_4",
                                          6: "rating_count_5"}, errors="raise")
    
    return df_product, df_rating
    
df1,df2 = scrapeProduct(limit, match_id, page_no)

df1 = df1.reset_index(drop=True)
df2 = df2.reset_index(drop=True)

print("df1",df1.shape)
print("df2",df2.shape)