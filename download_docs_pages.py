import sys
import requests
from bs4 import BeautifulSoup

ROOT_URL = "https://docs.microsoft.com/en-us/powerquery-m/"

CATEGORIES_LISTING_URL = "power-query-m-function-reference"

def main():
    filename = sys.argv[1]
    func_urls = [f for c in get_category_urls(fullurl(CATEGORIES_LISTING_URL)) for f in get_function_urls(c)]
    with open(filename, 'w') as f:
        f.write('\n'.join(func_urls))

soup = lambda url: BeautifulSoup(requests.get(url).content)
relurl = lambda tag: tag.attrs['href']
fullurl = lambda relurl: ROOT_URL + relurl
get_category_urls = lambda url: [fullurl(relurl(x)) for x in soup(url).find("main").find("h2").find_next_sibling('ul').find_all("a")]
get_function_urls = lambda url: [fullurl(relurl(x)) for x in soup(url).find("table").find("tbody").find_all("a")]



if __name__ == '__main__':
    main()
