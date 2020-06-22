import os

#Get list of Files
files=os.listdir('./')

#Filter out all files that do not end with '.AllUser'

filterFile=[]
for f in files:
    if f.endswith('.AllUser'):
        filterFile.append(f)
    
#Iterating over files
import pickle as pkl

#Getting the time stamp when each user entered each mental health community.
#initialize empty dictionary (I like dictionaries)
userEnter={}
#Getting the time stamp when each user left each mental health community.
#initialize empty dictionary (I like dictionaries)
userExit={}


#List of Subreddits 
SubList=['depression','bipolarreddit','mentalhealth','SuicideWatch','StopSelfHarm','EatingDisorder','selfanxiety','anxiety']

for d in filterFile:
    #print File Name
    print(d)
    #Open File as pickle
    file=pkl.load(open(d,"rb"))
    #iterating over the files
    for index, row in file.iterrows():
        user=row.author   # or user=row['author']

        #If a user is not in the dictionary userEnter, add them
        if user not in userEnter:
            #initialize empty dictionary
            userEnter[user]={}
        #If a user is not in the dictionary userExit, add them        
        if user not in userExit:
            #initialize empty dictionary
            userExit[user]={}

        subreddit=row.subreddit
        #Check if subreddit is a mental health subreddit
        if subreddit in SubList:
        
            #if subreddit is not in dictionary, add it
            if subreddit not in userEnter[user]:
                userEnter[user][subreddit]=row.created_utc
            if subreddit not in userExit[user]:
                userExit[user][subreddit]=row.created_utc
        
            #if current time is less than min time, update
            if row.created_utc < userEnter[user][subreddit]:
                userEnter[user][subreddit]=row.created_utc
                
            #if current time is greater than max time, update
            if row.created_utc < userExit[user][subreddit]:
                userExit[user][subreddit]=row.created_utc    
                
                
#Find the global min/max time for each user                