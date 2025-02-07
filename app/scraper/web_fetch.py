import requests
from bs4 import BeautifulSoup


def get_webpage(url: str) -> BeautifulSoup:
    page = requests.get(url).text
    
    soup = BeautifulSoup(page, 'html.parser')
    
    return soup


if __name__ == '__main__':

    soup = get_webpage('https://www.example.com')

    #print(soup.prettify())
    print(soup.text)