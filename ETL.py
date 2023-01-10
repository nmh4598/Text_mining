import tweepy
import pandas as pd
import sqlalchemy

client = tweepy.Client(bearer_token="")

query = '#airliquide'

tweets= tweepy.Paginator(client.search_recent_tweets, query=query,
                              tweet_fields=['context_annotations', 'created_at'], max_results=100).flatten(limit=1000)

df_id = []
df_tweet = []
df_date = []
for tweet in tweets:
       df_id.append(tweet.id)
       df_tweet.append(tweet.text)
       df_date.append(tweet.created_at)
list_of_tuples = list(zip(df_id , df_date, df_tweet))
df = pd.DataFrame(list_of_tuples, columns=['id', 'date', 'text'])
df.head(10)

URI = "mysql://root:master2@localhost/data"
con= sqlalchemy.create_engine(URI)
df["date"] = pd.to_datetime(df["date"], infer_datetime_format=True)
df.to_sql(name="floatrates", con=con, if_exists='append', index=False)