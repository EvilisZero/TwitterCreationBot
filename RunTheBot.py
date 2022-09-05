import persistqueue
import requests
import threading
import tweepy
import pandas as pd
import faker
import yaml
from glob import glob
import time
import random
from queue import Queue
from Twitter_Temp import controller
from Twitter_Temp_Proton import controller2
from Proxies import Proxy_splitter
from pymongo import MongoClient
tweets_number = 400
number_of_threads = 1
try:
    with open('old_accsst.txt', 'r') as f:
        acc = f.readlines()
except:
    pass

Hotmail = persistqueue.SQLiteQueue('HotMailACC', auto_commit=True, multithreading= True)
# if Hotmail.qsize() == 0:
#     with open('NewHotMail.txt', 'r') as f:
#         accs = f.readlines()
#     for acc in accs:
#         Hotmail.put(acc.strip("\n"))
config           = yaml.safe_load(open('config.yml'))
tweets_time      = int(config['Tweets_inbetween_time'])
number_of_tweets = int(config['Number_of_tweets_per_acc'])
tweet_Threads   = []
create_Threads  = []
tweets          = []
tweets1         = []
replies         = []
photos          = []
profile_picture = []
guest_token     = ''
reply_files     = glob('replies/*.txt')
tweets_files     = glob('tweets/*.txt')
tweets_files1    = glob('tweets1/*.txt')
profile_files    = glob('profile/*.jpg')
photos_files    = glob('photos/*.png')
for i in tweets_files:
    tweets.append(open(i,encoding='utf-8').read())
for i in tweets_files1:
    tweets1.append(open(i,encoding='utf-8').read())
for i in reply_files:
    replies.append(open(i,encoding="utf-8").read())
for i in profile_files:
    profile_picture.append(i)
for i in photos_files:
    photos.append(i)
with open('bio.txt', encoding='utf-8') as f:
    bio = f.readlines()
    f.close()
with open('location.txt', encoding='utf-8') as f:
    location = f.readlines()
    f.close()
wait_line       = Queue(maxsize=0)
try:
    for i in range(len(acc)):
        wait_line.put(acc[i])
except:
    pass


def guard(Threads):
     for thread in Threads:
        if thread.is_alive() == False:
            print('f')
            thread = threading.Thread(target=worker1,name="Thread "+str(t))
            Threads[t] = thread
            Threads[t].start()
            time.sleep(2)
        else:
            print('All threads are alive, checker is going to sleep for 60s')
            counterz = 0
        
def follow(API):
    for follower in tweepy.Cursor(API.search_users, q=faker.Faker().word()).items(15):
        time.sleep(0)
        try:
            API.create_friendship(screen_name=follower.screen_name)
        except:
            pass
def interact(user,API):
    time.sleep(1)
    print(user + 'is going to interact as it got search baned' )
    chance = random.choice(range(10))
    try:
        if chance == 3:
            follow(API)
        elif chance == 4:
            try:
                time.sleep(1)
                API.update_profile_image(random.choice(profile_picture))
            except Exception as e:
                print(e)
        elif chance == 5:
            try:
                API.update_profile(location = random.choice(location), description= random.choice(bio))
            except Exception as e:
                print(e)

        for tweet in tweepy.Cursor(API.search_tweets, q=faker.Faker().word(), result_type='recent').items(2):
            try:
                tweet_id = tweet.id_str
                b = [1,2,3]
                a = random.choice(b)
                if   a == 1:
                    API.create_favorite(tweet_id)
                elif a ==2:
                    tweet = str(faker.Faker().sentence())
                    API.update_status(status = tweet, in_reply_to_status_id = tweet_id , auto_populate_reply_metadata=True)
                else:
                    API.create_favorite(tweet_id)
                    time.sleep(3)
                    tweet = str(faker.Faker().sentence())
                    API.update_status(status = tweet, in_reply_to_status_id = tweet_id , auto_populate_reply_metadata=True)
                    time.sleep(3)
                    # API.retweet(id=tweet_id)
            except:
                pass
    except Exception as e:
        print(e)
    print(user)

def check(user, proxy):
    headers = {
    'authority': 'sbapi.lv5.ac:444',
    'accept': '*/*',
    'accept-language': 'en-US,en;q=0.9',
    'origin': 'https://shadowban.yuzurisa.com',
    'referer': 'https://shadowban.yuzurisa.com/',
    'sec-ch-ua': '".Not/A)Brand";v="99", "Google Chrome";v="103", "Chromium";v="103"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'cross-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',
}

    r = requests.get('https://sbapi.lv5.ac:444/' + user, proxies= {'http': 'htpp://' +proxy}, headers=headers)
    x = r.json()
    return x

def tweet(key,secret,proxy,user,aged):
        # print('tweeting')
        # replies_time     = int(config['Replies_inbetween_time'])
        auth1 = tweepy.OAuthHandler('3nVuSoBZnx6U4vzUxf5w', 'Bcs59EFbbsdF6Sl9Ng71smgStWEGwXXKSjYvPVt7qys')
        auth1.set_access_token(key, secret)
        API = tweepy.API(auth1,proxy= 'http://'  + proxy)
        tweet = tweet = str(faker.Faker().sentence()) 
        # for i in range(3):
        #     Tweet = API.update_status(status=tweet)
        #     time.sleep(i)
        time.sleep(2)
        if aged == False:
            follow(API)
            # interact(user,API)
            API.update_profile_image(random.choice(profile_picture))
            # API.update_profile(location = random.choice(location), description= random.choice(bio))
        try:
            for i in range(number_of_tweets):
                choice = True #random.choice([True,False])
                time.sleep(random.choice(range(2,5)))
                if choice:
                    try:
                        file = random.choice([1,2,3,4,5,6])
                        tweet_index = tweets_files.index('tweets\\'+str(file)+'.txt')
                        photo_index = photos_files.index('photos\\'+str(file)+'.png')
                        tweet = str(faker.Faker().sentence())+ '\n' + str(faker.Faker().sentence()) + tweets[tweet_index] + str(faker.Faker().word())
                        Tweet = API.update_status_with_media(status=tweet, filename=photos[photo_index])
                        print('tweeted')
                        print(Tweet.author.screen_name)
            
                    except Exception as e:
                        print(e) 
                        break   
                else:
                    try:
                        tweet = tweet = str(faker.Faker().sentence()) + '\n' + random.choice(tweets1)  + str(faker.Faker().word())
                        Tweet = API.update_status(status=tweet)
                    except:
                        break  
                if aged:
                    break
        except Exception as e:
            print(e)
            return False
        # try:
        #     status = check(user,proxy)
        #     if status['tests']['search'] == False:
        #         t = threading.Thread(target=interact, args=(user, API))
        #         t.start()
        #         print('account is search banned')
        # except:
        #     pass
        return True

def worker1():
    while True:
        if wait_line.empty():
            time.sleep(5)
            continue
        acc    = wait_line.get_nowait()
        try:
            aged   = False
            Key    = acc.split(':')[0]
            secret = acc.split(":")[1]
            user   = acc.split(':')[2]
            proxy  = str(acc.split(":")[5]) + ':' + str(acc.split(":")[6])
            what = tweet(Key,secret,proxy,user, aged)
            if what and aged:
                wait_line.put(acc)

        except Exception as e:
            print(e)
            wait_line.put(acc)
            pass

def worker2(thread):
    while True:
        Proxies    = True
        counterz   = 0
        Proxy_list = Proxy_splitter(number_of_threads)
        create     = controller(thread,Proxies,Proxy_list,Hotmail)
        acc        = create.mainTemp()
        wait_line.put(acc)
           
def worker3():
        connection_counter =0
        while connection_counter <= 5: 
                try:
                        uri = "mongodb+srv://Twitter_bot24368:ASDYRU24368@accountscluster.0ap1x.mongodb.net/myFirstDatabase?retryWrites=true&w=majority&ssl=true&ssl_cert_reqs=CERT_NONE"
                        client = MongoClient(uri, connect=True)
                except Exception as e:
                        print(e)
                        connection_counter += 1
                else:
                        print('\033[92m'+"The bot successfully connected to the database"+'\033[0m')
                        break
                
        database   = client["Accounts"]
        Proxies    = True
        counterz   = 0
        Proxy_list = Proxy_splitter(number_of_threads)
        create     = controller2(0,Proxies,Proxy_list,database)
        acc        = create.mainTemp()
        wait_line.put(acc)

if __name__ == "__main__":
    for i in range(tweets_number):
        thread = threading.Thread(target=worker1, name="Thread "+str(i))
        thread.start()
        tweet_Threads.append(thread)
    for i in range(number_of_threads):
        thread = threading.Thread(target=worker2, args=(i,),name="Thread "+str(i))
        thread.start()
        create_Threads.append(thread)
    # worker3()
    while True:
        try:
            time.sleep(60)
            t = 0
            # guard(tweet_Threads)
            guard(create_Threads)
        except:
            pass

