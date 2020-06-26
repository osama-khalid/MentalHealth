import os
import pickle as pkl

userList=open('userList','r').read().split('\n')[:-1]
validUser={}
for u in userList:
    row=u.split(',')
    validUser[row[0]]=[]
    validUser[row[0]].append(row[1])
    validUser[row[0]].append(row[2])
    validUser[row[0]].append(row[3])
    validUser[row[0]].append(row[4])
    
before={}
after={}
secondsYear=31536000     
#Get list of Files


commentFile='./Posts/'
files=os.listdir(commentFile)

#Filter out all files that do not end with '.AllUser'

filterFileComm=[]
for f in files:
    if f.endswith('.AllPosts'):
        filterFileComm.append(commentFile+f)

for d in filterFileComm:
    #print File Name

    print(d)
    #Open File as pickle
    file=pkl.load(open(d,"rb"))
    #iterating over the files
    for index, row in file.iterrows():
        user=row.author   # or user=row['author']
            
        if row.subreddit is not None:   
            if user in validUser:
                
                if row.created_utc<int(validUser[user][2]) and row.created_utc>int(validUser[user][2])-secondsYear/2:
                    if user not in before:
                        before[user]={}
                    if 'PostCount' not in before[user]:
                        before[user]['PostCount']=0
                    before[user]['PostCount']=before[user]['PostCount']+1
                    
                    if row.subreddit+'_p' not in before[user]:
                        before[user][row.subreddit+'_p']=0
                    before[user][row.subreddit+'_p']=before[user][row.subreddit+'_p']+1
                if row.created_utc>int(validUser[user][3]) and row.created_utc<int(validUser[user][3])+secondsYear/2:
                    if user not in after:
                        after[user]={}
                    if 'PostCount' not in after[user]:    
                        after[user]['PostCount']=0
                    after[user]['PostCount']=after[user]['PostCount']+1
                        
                    if row.subreddit+'_p' not in after[user]:
                        after[user][row.subreddit+'_p']=0
                    after[user][row.subreddit+'_p']=after[user][row.subreddit+'_p']+1
                        
                    
                    
commentFile='./Comments/'
files=os.listdir(commentFile)

#Filter out all files that do not end with '.AllUser'

filterFileComm=[]
for f in files:
    if f.endswith('.AllUser'):
        filterFileComm.append(commentFile+f)

for d in filterFileComm:
    #print File Name

    print(d)
    #Open File as pickle
    file=pkl.load(open(d,"rb"))
    #iterating over the files
    for index, row in file.iterrows():
        user=row.author   # or user=row['author']
            
        if row.subreddit is not None and row.subreddit !='reddit.com':
            if user in validUser:
                
                if row.created_utc<int(validUser[user][2]) and row.created_utc>int(validUser[user][2])-secondsYear/2:
                    if user not in before:
                        before[user]={}
                    if 'CommentCount' not in before[user]:
                        before[user]['CommentCount']=0
                    before[user]['CommentCount']=before[user]['CommentCount']+1
                    
                    if row.subreddit+'_c' not in before[user]:
                        before[user][row.subreddit+'_c']=0
                    before[user][row.subreddit+'_c']=before[user][row.subreddit+'_c']+1
                if row.created_utc>int(validUser[user][3]) and row.created_utc<int(validUser[user][3])+secondsYear/2:
                    if user not in after:
                        after[user]={}
                    if 'CommentCount' not in after[user]:    
                        after[user]['CommentCount']=0
                    after[user]['CommentCount']=after[user]['CommentCount']+1
                        
                    if row.subreddit+'_c' not in after[user]:
                        after[user][row.subreddit+'_c']=0
                    after[user][row.subreddit+'_c']=after[user][row.subreddit+'_c']+1

data=[before,after]
filehandler = open("behave.obj","wb")
pkl.dump(data,filehandler)                    