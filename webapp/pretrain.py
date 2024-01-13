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


# reviews = scrapped[1] 
# ratings = []
# filename = 'data/{}.csv'.format(scrapped[0][0])
# with open (filename, 'w') as f: 
#     w = csv.writer(f, delimiter=',')
#     w.writerow(['itemid','username','userid', 'ctime', 'rating','comment','fakeornot', 'confidence level'])
#     for review in reviews: 
#         review.extend([0,0])
#         w.writerow(review)

filename = 'data/raiyanlys.sg.csv'

final_review = pretrain(filename)
print(final_review)