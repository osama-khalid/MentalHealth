import os
import sys    
sys.path.insert(0, 'lib')
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="./keys.json"

from google.cloud import bigquery
#os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = KEY
client = bigquery.Client()
from google.oauth2 import service_account

import pandas as pd
from tqdm import tqdm
import pickle as pkl
import numpy as np
import importlib
#import utils

#START = '2015_01'
#END = '2019_05'

WRITE = 'wb'
READ = 'rb'

#M = utils.months(START, END)
#ALL_MONTHS = utils.months('2001_01', '2020_01')
ALL_MONTHS=['2019_01']




credentials = service_account.Credentials.from_service_account_file("./keys.json",)


subs = pkl.load(open('subreddits.list', 'rb'))
subreddits = pd.DataFrame()
subreddits['subreddit'] = subs
#subreddits=subreddits[:1]
subreddits['subreddit'][0]='depression'
#subreddits=subreddits[:1]

# reference_subreddits.to_gbq('reddit.new_reference_subreddits', 'lums-reddit', private_key=KEY, if_exists='replace')
subreddits.to_gbq('subreddits.all', project_id="amiable-parser-247511", credentials=credentials, if_exists='replace')

#print(halp)



query = '''
SELECT
  r.*
FROM
  `fh-bigquery.reddit_comments.%s` as r
  INNER JOIN 
  `amiable-parser-247511.subreddits.all` as s
  ON r.subreddit = s.subreddit
WHERE
  RAND() > 0.90'''

for m in tqdm(ALL_MONTHS):
    try:
        q = query % m
        df = pd.read_gbq(q,project_id="amiable-parser-247511" , credentials=credentials, dialect='standard')
        print(q)
        df.to_pickle('123')
    except:
        pass
    