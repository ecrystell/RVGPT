import requests

data = requests.get("https://shopee.sg/api/v2/shop/get_shop_detail?shopid=106973794")

print(data.json())