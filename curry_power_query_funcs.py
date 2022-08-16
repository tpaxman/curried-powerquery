import requests
from bs4 import BeautifulSoup

ROOT_URL = "https://docs.microsoft.com/en-us/powerquery-m/"

CATEGORIES_RELPATH = "power-query-m-function-reference"

def main():
    categories_pages = find_category_pages(ROOT_URL + CATEGORIES_RELPATH)
    function_pages = {name: url for x in categories_pages.values() for name, url in find_function_pages(x).items()}
    function_signatures = {name: find_function_signature(url) for name, url in function_pages.items()}
    pieces = {k: parse_signature(v) for k, v in function_signatures.items()}
    data = (
        pd.DataFrame(pieces).transpose().rename(columns=dict(enumerate(('funcname', 'first_arg', 'other_args', 'return_type'))))
        .assign(
            curry_funcname = lambda df: df.funcname.str.replace('.', '_', regex=False).str.lower(),
            curried_func = lambda t: t.curry_funcname + ' = (' + t.other_args + ') as function => (' + t.first_arg + ') ' + t.return_type
        )
    )

    
def find_category_pages(listing_url: str) -> list:
    return {x.text: form_fullpath(x.attrs['href']) for x in soupify(listing_url).find(id='main').find('ul', attrs={'class': None}).find_all('a')}


def find_function_pages(category_url: str) -> list:
    links = [first_col.find('a') for x in soupify(category_url).find_all('tr') if (first_col := x.find('td'))]
    relpaths = {x.text: form_fullpath(x['href']) for x in links if x}
    return relpaths


def find_function_signature(function_page_url: str) -> str:
    soup = soupify(function_page_url)
    text = pre.text.strip() if (pre := soup.find('pre')) else ''
    print(text)
    return text

    
def parse_signature(function_signature: str) -> dict:
    found_stuff = re.findall(r'(\#*[\w.]+)\s*\(([^,]*),*\s*([^\)]*)\)\s*(.*)', function_signature)
    return found_stuff[0] if found_stuff else ('', '', '', '')
    #name, first_arg, other_args, return_type = re.findall(r'(\w+\.\w+)\(([^,]+),*\s*([^\)]*)\)\s*(.*)',  function_signature)[0]
    #return {'name': name, 'first_arg': first_arg, 'other_args': other_args, 'return_type': return_type}


def soupify(url: str) -> BeautifulSoup:
    return BeautifulSoup(requests.get(url).content)


def form_fullpath(relpath: str) -> str:
    return ROOT_URL + relpath



if __name__ == '__main__':
    main()
