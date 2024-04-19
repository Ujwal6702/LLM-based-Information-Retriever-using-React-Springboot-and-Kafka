import requests
from bs4 import BeautifulSoup as bs

def google_search(query):
    url = f"https://www.google.com/search?q={'+'.join(query.split())}"
    headers = {
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:78.0) Gecko/20100101 Firefox/78.0",
                "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,/;q=0.8,application/signed-exchange;v=b3;q=0.9",
                'sec-fetch-site': 'none',
                'sec-fetch-mode': 'navigate',
                'sec-fetch-user': '?1',
                'sec-fetch-dest': 'document',
                'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
            }

    response = requests.get(url, headers=headers)
    soup = bs(response.text, 'html.parser')
    return soup.get_text()


if __name__=="__main__":
    print(google_search("RR vs RCB Score"))