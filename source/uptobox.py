import requests
import urllib.parse

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





# def uptobox(url):
#     headers = {
#         'cookie': 'xfss=prmmlbgvakv3bunn'
#     }
#     proxy = gibe_random_proxy()
#     try:
#         print('hero')
#         temp = requests.get(url, headers=headers, allow_redirects=False, proxies=proxy)
#         if temp.status_code == 302:
#             return temp.headers['location']
#         else:
#             return False
#     except:
#         print('there')
#         return uptobox(url)


def uptobox(url):
    url_generate = f'http://uptobox.playthis.site:45990/file/generate/?uptobox_link={url}'
    try:
        response = requests.get(url_generate)
        print(response.text)
        if response.status_code == 200:
            return response.json().get('download', False)
    except Exception as err:
        print(f'exception uptobox - {err}')
    return False