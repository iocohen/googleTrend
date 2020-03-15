from pytrends.request import TrendReq
from datetime import date
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import datetime
import sys
import os
import argparse
import pathlib
import uuid

date = datetime.datetime.now()

ap = argparse.ArgumentParser()
ap.add_argument("-q", "--query", required=True, help="insert your word")

ap.add_argument("-c", "--country", required=False, help="country to search on")

args = ap.parse_args()

key_word = args.query
country = args.country
day = '2020-02-01 ' + datetime.datetime.today().strftime('%Y-%m-%d')

pytrends = TrendReq(hl='en-US', tz=360)
pytrends.build_payload(
    [key_word], cat=0, timeframe=day,  gprop='', geo=country)
df = pytrends.interest_over_time()

print(df.head())

unique_filename = str(uuid.uuid4())

result = '%s-%s-%s_%s' % (date.year, date.month, date.day, unique_filename)
sns.set()
df['timestamp'] = pd.to_datetime(df.index)
sns.lineplot(df['timestamp'], df[key_word])

if country is None:
	plt.title("The global trend of " + key_word)
	name =   key_word + result+ ".png"
else:
	plt.title("The trend of  " + key_word + "  in " + country)
	name =   country + key_word + result + ".png"


plt.ylabel("Number of Searches of " + key_word)
plt.xlabel("Date")
plt.xticks(rotation=45)

filepath = pathlib.Path(__file__).resolve().parent

path = os.path.join(filepath, name)

plt.savefig(path)
plt.show()
