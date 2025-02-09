import requests
from bs4 import BeautifulSoup


def get_webpage(url: str) -> BeautifulSoup:
    print('Soupifying ' + url)
    page = requests.get(url).text
    soup = BeautifulSoup(page, 'html.parser')
    return soup


def handle_pocket_tactics(soup: BeautifulSoup) -> list[dict[str, str]]:
    print('Handling a pocket tactics page')
    
    # the first ul is usually the one that contains the list of codes
    ul_codes = soup.css.select('.entry-content ul')[0]
    
    lis = ul_codes.select('li')
    codes = []
    
    for li in lis:
        code = li.select('strong')[0].text
        
        # this gets "CODE - rewards" and it will always be the last part
        rewards = li.text.split(' – ')[-1] # this is not the simple minus symbol

        codes.append({
            'code': code,
            'rewards': rewards
        })
        
    return codes


def handle_antifandom(soup: BeautifulSoup) -> list[dict[str, str]]:
    pass


def extract_codes(url: str) -> list[dict[str, str]] | list[None]:
    print('Attempting to get codes from: ' + url)
    
    soup = get_webpage(url)
    
    if 'pocket' in url:
        return handle_pocket_tactics(soup)
    else:
        print('No valid sites passes, returning empty array')
        return []


if __name__ == '__main__':
    
    codes = extract_codes('https://www.pockettactics.com/wuthering-waves/codes')
    
    for code in codes:
        print(code)