import os
import sys    
sys.path.insert(0, 'lib')
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="./keys.json"
#pip install google-cloud-bigquery
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
ALL_MONTHS=['2019_01','2019_02','2019_03','2019_04','2019_05','2019_06','2019_07','2019_08','2015_12'
,'2016_01','2016_02','2016_03','2016_04','2016_05','2016_06','2016_07','2016_08','2016_09','2016_10','2016_11','2016_12'
,'2017_01','2017_02','2017_03','2017_04','2017_05','2017_06','2017_07','2017_08','2017_09','2017_10','2017_11','2017_12'
,'2018_01','2018_02','2018_03','2018_04','2018_05','2018_06','2018_07','2018_08','2018_09','2018_10','2018_11','2018_12']
#'''




credentials = service_account.Credentials.from_service_account_file("./keys.json",)


subs = pkl.load(open('subreddits.list', 'rb'))
subreddits = pd.DataFrame()
subreddits['subreddit'] = subs
#subreddits=subreddits[:1]
subreddits['subreddit'][0]='WritingPrompts'
#subreddits=subreddits[:1]
Subs=['depression','bipolarreddit','mentalhealth','SuicideWatch','StopSelfHarm','EatingDisorder','selfanxiety','anxiety']

# reference_subreddits.to_gbq('reddit.new_reference_subreddits', 'lums-reddit', private_key=KEY, if_exists='replace')
subreddits.to_gbq('subreddits.all', project_id="amiable-parser-247511", credentials=credentials, if_exists='replace')

#print(halp)



query = '''
SELECT
  r.*
FROM
  `fh-bigquery.reddit_posts.%s` as r
Where r.subreddit='%s';

'''
'''
WHERE
  RAND() > 0.90
'''
for S in Subs:
    for m in tqdm(ALL_MONTHS):
        try:
            q = query % (m,S)
            df = pd.read_gbq(q,project_id="amiable-parser-247511" , credentials=credentials, dialect='standard')
            print(q)
            df.to_pickle(m+'_'+S+'.posts')
        except:
            pass
    