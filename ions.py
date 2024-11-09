import re

import genanki
import pandas as pd
import requests
from bs4 import BeautifulSoup

from anki_models.anki_ids import GEN_CHEM_ID


PATH = 'https://gchem.cm.utexas.edu/canvas.php?target=bonding/ionic/polyatomic-ions.html'

def get_ions():
    """Get the polyatomic ions from the UTexas website."""
    with requests.get(PATH) as response:
        soup = BeautifulSoup(response.text, 'html.parser')
        tables = soup.find_all('table')
        df_ions = pd.DataFrame(columns=['Name', 'Formula'])
        for table in tables:
            df = pd.read_html(str(table))[0]
            if 'IUPAC Name' in df.columns:
                df_older = df[['older name', 'Formula']].rename(columns={'older name': 'Name'})
                df = df.drop(columns=['older name']).rename(columns={'IUPAC Name': 'Name'})
                df = pd.concat([df, df_older])
            df_ions = pd.concat([df_ions, df])

    # Fix acetate
    df_ions = df_ions.replace('acetate acetate', 'acetate')
    df_ions.loc[df_ions['Name'] == 'acetate', 'Formula'] = 'C2H3O2− OR CH3COO−'
    df_ions = df_ions.reset_index(drop=True)

    # Fix charges
    df_ions['Formula'] = df_ions['Formula'].str.replace('−', '-')

    return df_ions


def fix_formula(formula):
    """Format the chemical formula with HTML sub and sup tags."""

    # Replace numbers following an element with <sub> (e.g., H2O -> H<sub>2</sub>O)
    formula = re.sub(r'([A-Za-z])(\d{1})', r'\1<sub>\2</sub>', formula)

    # Replace charges with <sup> (e.g., SO4 2- -> SO<sub>4</sub><sup>2-</sup>)
    formula = re.sub(r'(\d{0,1}[-+])', r'<sup>\1</sup>', formula)

    return formula


def main():
    """Generate the polyatomic ions deck."""
    df_ions = get_ions()
    df_ions['Formula'] = df_ions['Formula'].apply(fix_formula)

    deck = genanki.Deck(GEN_CHEM_ID, 'Science::General Chemistry::Polyatomic Ions')
    for _, row in df_ions.iterrows():
        note = genanki.Note(model=genanki.BASIC_MODEL, fields=[row['Name'], row['Formula']])
        deck.add_note(note)

    genanki.Package(deck).write_to_file('polyatomic_ions.apkg')
    return df_ions


if __name__ == '__main__':
    df = main()
    print(df)