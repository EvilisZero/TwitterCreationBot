import email
import requests
import re
import datetime
from queue import Queue
from requests_oauthlib import OAuth1
import time
import random
import threading
try:
    with open('old_accss.txt', 'r') as f:
        acc = f.readlines()
except:
    pass
try:
    with open('proxies.csv', 'r') as f:
        proxies = f.readlines()
except:
    pass
wait_line       = Queue(maxsize=0)
try:
    for i in range(len(acc)):
        wait_line.put(acc[i])
except:
    pass
now = datetime.datetime.now().time()
def guest_activate():
    headers = {
        'Authorization': 'Bearer AAAAAAAAAAAAAAAAAAAAAAj4AQAAAAAAPraK64zCZ9CSzdLesbE7LB%2Bw4uE%3DVJQREvQNCZJNiz3rHO7lOXlkVOQkzzdsgu6wWgcazdMUaGoUGm'}
    counter = 0
    while counter < 5:
        try:
            http = 'https'
            response = requests.post('https://api.twitter.com/1.1/guest/activate.json' ,proxies={http: 'http://' + 'p.webshare.io:9999', 'http': 'http://' + 'p.webshare.io:9999'},headers=headers,verify=False)
            if b'Rate limit exceeded' in response.content:
                print('Rate limit exceeded')
                break
            guest_token = response.json()['guest_token']
            break
        except Exception as e:
            print(e)
    return guest_token

def get_access(user,Pass, user_id, request_id, proxy):
    global proxies
    url = 'https://api.twitter.com/oauth/access_token'
    data = 'x_auth_mode=client_auth&x_auth_login_verification=1&x_auth_login_challenge=1&send_error_codes=true&login_verification_user_id=' + user_id + '&login_verification_request_id=' + request_id
    url2 = url + '?' + data
    auth = OAuth1('IQKbtAYlXLripLGPWd0HUA', 'GgDYlkSvaPxGxC4X8liwpUoqKwwr3lCADbz8A7ADU')
    http = 'https'
    while 1:
        try:
            response = requests.get(url2, auth=auth, proxies={http: 'http://' + proxy}, verify=False)
            break
        except Exception as e:
            print('retrying ...', e)

    tweets = response.json()
    if 'oauth_token' in tweets:
        return tweets
    else:
        return False

def login_challenge2(User, Pass, data, url, twt_sess, personalization_id, proxy,guest_token):
    cookies = {'guest_id': 'v1%3A' + guest_token,
        '_twitter_sess': twt_sess,
        'lang': 'en'}
    headers = {'Host': 'twitter.com',
        'Connection': 'close',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Origin': 'https://twitter.com',
        'User-Agent': 'Mozilla/5.0 (Linux; Android 4.4.2; SM-G955N Build/NRD90M) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/30.0.0.0 Mobile Safari/537.36',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Referer': url,
        'Accept-Encoding': 'gzip,deflate',
        'Accept-Language': 'en-EG,en-US;q=0.8',
        'X-Requested-With': 'com.twitter.android'}
    data = data
    iiii = 0
    http = 'https'
    while 1:
        try:
            response = requests.post('https://twitter.com/account/login_challenge', proxies={http: 'http://' + proxy}, headers=headers, cookies=cookies, data=data, allow_redirects=False, verify=False)
            l = response.headers['location']
            break
        except:
            print('Requesting Error For Challenge ')
            print('retrying ...')
            iiii += 1
            if iiii >= 5:
                break
    if 'success' in response.headers['location']:
        print('challenge Completed.')
        request_id = data.split('challenge_id=')[1].split('&')[0]
        user_id = data.split('user_id=')[1].split('&')[0]
        return get_access(User,Pass, user_id, request_id, proxy)
    else:
        print('challenge Failed.')
        return False

def login_challenge(url, User, Pass, proxy,guest_token,Email):
    cookies = {'guest_id': 'v1%3A' + guest_token}
    headers = {'Host': 'twitter.com',
                'Connection': 'close',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'User-Agent': 'Mozilla/5.0 (Linux; Android 4.4.2; SM-G955N Build/NRD90M) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/30.0.0.0 Mobile Safari/537.36',
                'Accept-Encoding': 'gzip,deflate',
                'Accept-Language': 'en-EG,en-US;q=0.8',
                'X-Requested-With': 'com.twitter.android'}
    http = 'https'
    counter = 0
    while 1:
        try:
            response = requests.get(url, proxies={http: 'http://' + proxy}, headers=headers, cookies=cookies,
                                    verify=False)
            break
        except Exception as e:
            print('retrying ...', e)
            if counter < 5:
                continue
            else:
                break
    twt_sess = response.headers['set-cookie'].split('_twitter_sess=')[1].split(';')[0]
    personalization_id = ''
    values = re.findall('type="hidden" name=".*" value=".*"', response.text)
    data = ''
    for val in values:
        if data != '':
            data += '&'
        name = val.split('name="')[1].split('" value')[0]
        value = val.split('value="')[1].split('"')[0]
        data += name + '=' + value
    data += '&challenge_response=' + Email
    return login_challenge2(User,Pass, data, url, twt_sess, personalization_id, proxy,guest_token)

def access(proxy, User, Pass,Email,guest_token):
    Tokens = []
    headers = {'X-Guest-Token': guest_token, 'Accept-Language': 'en-EG',
                'Authorization': 'Bearer AAAAAAAAAAAAAAAAAAAAAAj4AQAAAAAAPraK64zCZ9CSzdLesbE7LB%2Bw4uE%3DVJQREvQNCZJNiz3rHO7lOXlkVOQkzzdsgu6wWgcazdMUaGoUGm',
                'Content-Type': 'application/x-www-form-urlencoded'}
    data = {'x_auth_identifier': User,
            'x_auth_password': Pass,
            'send_error_codes': 'true',
            'x_auth_login_verification': '1',
            'x_auth_login_challenge': '1',
            'x_auth_country_code': 'EG'}
    http = 'https'
    response = requests.post('https://api.twitter.com/auth/1/xauth_password.json',proxies={http: 'http://' + proxy, 'http': 'http://' + proxy}, headers=headers,data=data, timeout=5, verify=False)
    r = response
    x = response.json()
    print(x)
    if b'Bad guest token' in response.content:
        try:
            guest_activate()
        except Exception as e:
            print(e)
    if b'oauth_token' in response.content:
        print('Login Success.')
        responsee = x['oauth_token'] + ':' + x['oauth_token_secret'] + User + ":" + Pass + proxy

        save = open('Access.txt', 'a+')
        save.write(responsee + '\n')
        save.close()
    if b'login_verification_request_url' in response.content:
        print('challenge Required.')
        lvr_url = x['login_verification_request_url']
        try:
            x = login_challenge(lvr_url, User,Pass, proxy,guest_token,Email)
            
        except Exception as e:
            print(e)
            try:
                x = login_challenge(lvr_url, User,Pass, proxy,guest_token,Email)
            except Exception as e:
                print(e)
                print('challenge Error Happenned.')
                responsee = False
    Tokens.append(x['oauth_token'])
    Tokens.append(x['oauth_token_secret'])
    print(Tokens)
    return Tokens

def worker1():
    while True:
        acc    = wait_line.get_nowait().split(':')
        guest_token = guest_activate()
        user     = acc[0]
        print(user)
        password = acc[1]
        email    = acc[2]
        proxy  = random.choice(proxies)
        n = 0
        while n < 5:
                try:
                    tokens = access(proxy,user, password,email,guest_token)
                            # Thread.join()
                    time.sleep(0)
                    with open('access_old_acc.txt', 'a') as f:
                        f.writelines(tokens[0] + ':' + tokens[1] + '\n' )
                        f.close()
                    break
                    
                except Exception as e:
                    n +=1
                    proxy = random.choice(proxies)
                    continue
        time.sleep(2)
if __name__ == "__main__":
    for i in range(5):
        Thread = threading.Thread(target=worker1, name=i)
        Thread.start()
