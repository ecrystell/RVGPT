from flask import Flask, render_template

app = Flask(__name__)

import rvgpt    

@app.route('/index/')
@app.route('/')
def index():
  
    reviews = rvgpt.final_review
    fraud = rvgpt.fradulent

    if fraud[0][0] > 0.7: 
        seller = "This seller is very reliable"
    elif fraud[0][0] > 0.5:
        seller = "This seller is likely reliable"
    elif fraud[0][0] > 0.3:
        seller = "This seller has a risk of engaging in fradulent activities"
    else: 
        seller = "This seller has a high risk of engaging in fradulent activities"

    review = 'There are {} fake reviews'.format(str(reviews[0]))

    # seller = 0.5
    # review = '0 fake reviews'

    return render_template('index.html', seller = seller, reviews = review)

if __name__ == "__main__":
    app.run(debug=True)
