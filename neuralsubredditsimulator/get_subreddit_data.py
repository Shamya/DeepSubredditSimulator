#comma_symbol
#save submissions as pickle date wise
#get posts
import praw, re, csv, sys

NAME = "data/post_explainlikeimfive.csv"
# r = praw.Reddit(user_agent='test_dss')
r = praw.Reddit(user_agent='NNSubredditSimulator',
                client_id='P2LTafib7wqlvw',
                client_secret=' qZOs4UWiVa-AXFWo_UX6dWYYdeA')

submissions_new = r.subreddit('explainlikeimfive').new(limit=10)
submissions_hot = r.subreddit('explainlikeimfive').hot(limit=10)
print(submissions_new)

for submission in submissions_new:
  print(submission)

sys.exit()

ids = []
with open(NAME, 'rb') as fn:
    reader = csv.reader(fn)#, delimiter=' ', quotechar='|')
    #avoid duplicates
    for row in reader:
        ids.append(row[0])

with open(NAME, 'a') as fn:
    for sub in submissions_new:
        txt = sub.selftext.encode('utf-8')
        txt_title = sub.title.encode('utf-8')
        if len(txt) > 0 and sub.id not in ids:
            #add to list to avoid duplicate
            ids.append(sub.id)
            txt = re.sub('\n', ' ', txt)
            txt = re.sub(',', 'comma_symbol', txt)
            txt_title = re.sub('\n', ' ', txt_title)
            txt_title = re.sub(',', 'comma_symbol', txt_title)
            try:
                fn.write ('\n'+sub.id+','+sub.url.encode('utf-8')+','+txt_title+','+str(sub.ups)+','+str(sub.downs)+','+str(sub.score)+','+sub.permalink.encode('utf-8')+','+str(sub.num_comments)+','+str(sub.media)+','+str(sub.created_utc)+','+sub.author.name.encode('utf-8')+','+txt)
            except:
                print "skipped"
    
    for sub in submissions_hot:
        txt = sub.selftext.encode('utf-8')
        txt_title = sub.title.encode('utf-8')
        if len(txt) > 0 and sub.id not in ids:
            txt = re.sub('\n', ' ', txt)
            txt = re.sub(',', 'comma_symbol', txt)
            txt_title = re.sub('\n', ' ', txt_title)
            txt_title = re.sub(',', 'comma_symbol', txt_title)
            try:
                fn.write ('\n'+sub.id+','+sub.url.encode('utf-8')+','+txt_title+','+str(sub.ups)+','+str(sub.downs)+','+str(sub.score)+','+sub.permalink.encode('utf-8')+','+str(sub.num_comments)+','+str(sub.media)+','+str(sub.created_utc)+','+sub.author.name.encode('utf-8')+','+txt)
            except:
                print "skipped"