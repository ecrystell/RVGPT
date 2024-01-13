from flask import Flask, render_template

app = Flask(__name__)

import rvgpt    
import csv

url = rvgpt.url
print(url)
scrapped = rvgpt.scrapesite(url, True)

reviews = scrapped[1] 
filename = 'data/{}.csv'.format(scrapped[0][0])
with open (filename, 'w') as f: 
    w = csv.writer(f, delimiter=',')
    w.writerow(['itemid','username','userid', 'ctime', 'rating','comment','fakeornot', 'confidence level'])
    for review in reviews: 
        review.extend([0,0])
        w.writerow(review)

reviews = rvgpt.pretrain(filename)
print(reviews)

seller = scrapped[0] 
seller = scrapped[0]     
rvgpt.clean(seller)
print(seller)
fraud = rvgpt.seller_fraud(seller[1], seller[2], seller[3], seller[4], seller[5])

@app.route('/index/')
@app.route('/')
def index():

    seller = float(fraud[0][0])

    review = 'There are {} fake reviews'.format(str(reviews[0]))

    # seller = 0.5
    # review = '0 fake reviews'

    return render_template('index.html', seller = seller, reviews = review)

if __name__ == "__main__":
    app.run(debug=True)
