import requests


def gibe_random_proxy():
    return {}



def download_from_uptobox(url):
    response_premium = uptobox(url, cookie)
    if response_premium.status_code == 302:
        url_premium = response_premium.headers['location']
        name = url_premium[url_premium.rindex('/')+1:]
        if os.path.isfile(name) == False:
            r = requests.get(url_premium, allow_redirects=True)
            with open(name, 'wb') as f:
                f.write(r.content)
            return name
        else:
            return name
    else:
        return False





def uptobox(url):
    headers = {
        'cookie': 'xfss=prmmlbgvakv3bunn'
    }
    proxy = gibe_random_proxy()
    try:
        print('hero')
        temp = requests.get(url, headers=headers, allow_redirects=False, proxies=proxy)
        if temp.status_code == 302:
            return temp.headers['location']
        else:
            return False
    except:
        print('there')
        return uptobox(url)