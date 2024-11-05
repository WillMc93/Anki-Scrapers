import requests
from bs4 import BeautifulSoup
import genanki

from shared import BASE_URI
from anki_models.anki_ids import GEN_CHEM_ID_RANGE
from anki_models.definition_model import definition_model

CHEMISTRY_URL = f'{BASE_URI}/chemistry-2e'

#%%
def get_terms(chapter: int):
    """Scrape the OpenStax Chemistry 2e Key Terms"""

    url = f'{CHEMISTRY_URL}/pages/{chapter}-key-terms'
    response = requests.get(url)
    response.raise_for_status()
    response.encoding = 'utf-8'  # Ensure the response is interpreted as UTF-8

    soup = BeautifulSoup(response.text, 'html.parser')
    glossary = soup.find('div', class_='os-eoc os-glossary-container')
    terms = glossary.find_all('dl')

    for dl in terms:
        term = dl.find('dt').decode_contents()
        definition = dl.find('dd').decode_contents()

        # Handle Greek symbols and em tags
        term = BeautifulSoup(term, 'html.parser').get_text()
        definition = BeautifulSoup(definition, 'html.parser').get_text()

        # Handle apostrophes
        term = term.replace("’", "'")
        definition = definition.replace("’", "'")

        yield term, definition


#%%
if __name__ == '__main__':
    decks = []
    for i in range(2, 21):
        # Make Deck
        deck = genanki.Deck(
            GEN_CHEM_ID_RANGE[i],
            f'Science::General Chemistry::Chapter {i if i > 9 else f"0{i}"}'
        )
        for term, definition in get_terms(i):
            print(f'{term}: {definition}')

            # Make Anki card
            note = genanki.Note(
                model=definition_model,
                fields=[term, definition],
                tags=[f'Chapter_{i if i > 9 else f"0{i}"}']
            )
            deck.add_note(note)
        decks.append(deck)
    genanki.Package(decks).write_to_file('gen_chem.apkg')