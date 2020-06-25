import os
'''
Creates List of Vaid Users of the form
UserName,First_Post,Last_Post,StartofIntervention,EndofIntervention
'''
#Get list of Files
commentFile='./Comments/'
files=os.listdir(commentFile)

#Filter out all files that do not end with '.AllUser'

filterFileComm=[]
for f in files:
    if f.endswith('.AllUser'):
        filterFileComm.append(commentFile+f)
        
postFile='./Posts/'
files=os.listdir(postFile)

#Filter out all files that do not end with '.AllUser'

filterFilePost=[]
for f in files:
    if f.endswith('.AllPosts'):
        filterFilePost.append(postFile+f)
            
    
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

#CountNumberofPosts
userCount={}
userFirst={}
userLast={}
for d in filterFileComm:
    #print File Name

    print(d)
    #Open File as pickle
    file=pkl.load(open(d,"rb"))
    #iterating over the files
    for index, row in file.iterrows():
        user=row.author   # or user=row['author']
        if user not in userFirst:
            userFirst[user]=row.created_utc
        if user not in userLast:
            userLast[user]=row.created_utc
        if row.created_utc<userFirst[user]:
            userFirst[user]=row.created_utc
        if row.created_utc>userLast[user]:
            userLast[user]=row.created_utc
        subreddit=row.subreddit
        #Check if subreddit is a mental health subreddit
        if subreddit in SubList:
            
            

            #If a user is not in the dictionary userEnter, add them
            if user not in userEnter:
                #initialize empty dictionary
                userEnter[user]={}
            #If a user is not in the dictionary userExit, add them        
            if user not in userExit:
                #initialize empty dictionary
                userExit[user]={}

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
                
                
            #Counting number of posts in MH community by user    
            if user not in userCount:
                userCount[user]=0
            userCount[user]=userCount[user]+1
#Find the global min/max time for each user                


for d in filterFilePost:
    #print File Name

    print(d)
    #Open File as pickle
    file=pkl.load(open(d,"rb"))
    #iterating over the files
    for index, row in file.iterrows():
        user=row.author   # or user=row['author']
        if user not in userFirst:
            userFirst[user]=row.created_utc
        if user not in userLast:
            userLast[user]=row.created_utc
        if row.created_utc<userFirst[user]:
            userFirst[user]=row.created_utc
        if row.created_utc>userLast[user]:
            userLast[user]=row.created_utc
        subreddit=row.subreddit
        #Check if subreddit is a mental health subreddit
        if subreddit in SubList:
            
            

            #If a user is not in the dictionary userEnter, add them
            if user not in userEnter:
                #initialize empty dictionary
                userEnter[user]={}
            #If a user is not in the dictionary userExit, add them        
            if user not in userExit:
                #initialize empty dictionary
                userExit[user]={}

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
                
                
            #Counting number of posts in MH community by user    
            if user not in userCount:
                userCount[user]=0
            userCount[user]=userCount[user]+1
#Find the global min/max time for each user                


users={}            #users[username][min,max]
for u in userExit:
    if u not in users:
        users[u]=[float('inf'),0]
    for com in userEnter[u]:
        if int(userEnter[u][com])<users[u][0]:
            users[u][0]=int(userEnter[u][com])
    for com in userExit[u]:
        if int(userExit[u][com])>users[u][1]:
            users[u][1]=int(userExit[u][com])

secondsYear=31536000    #Seconds in year
#Get users who have posted for more than six months
validUsers={}
for u in users:
    if (users[u][1]-users[u][0])>(secondsYear/4):   #If user's MH lifespan is more than 6 months
        if userCount[u]>5:#if user has posted more than 10 times
            validUsers[u]=users[u]
            
            
file=open('userList','w')
for v in validUsers:
    file.write(v+','+str(userFirst[v])+','+str(userLast[v])+','+str(validUsers[0])+','+str(validUsers[1])+'\n')