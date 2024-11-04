import requests
from bs4 import BeautifulSoup

from shared import BASE_URI


CHEMISTRY_URL = f'{BASE_URI}/chemistry-2e'

#%%
def get_terms(chapter:int) -> dict:
    """Scrape the OpenStax Chemistry 2e Key Terms"""

    url = f'{CHEMISTRY_URL}/pages/{chapter}-key-terms'
    response = requests.get(url)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, 'html.parser')
    glossary = soup.find('div', class_='os-eoc os-glossary-container')
    terms = glossary.find_all('dl')

    for dl in terms:
        term = dl.find('dt')
        definition = dl.find('dd')
        yield term.text, definition.text

#%%
if __name__ == '__main__':
    for i in range(1, 21):
        for term, definition in get_terms(i):
            print(f'{term}: {definition}')