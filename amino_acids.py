import re

import genanki
import pandas as pd
import requests
from bs4 import BeautifulSoup

from anki_models.anki_ids import AMINO_ACIDS_ID

AA_PATH = 'https://www.vanderbilt.edu/AnS/Chemistry/Rizzo/stuff/AA/AminoAcids.html'

def get_amino_acids():
    """Get the amino acids from the Vanderbilt website."""
    with requests.get(AA_PATH) as response:
        soup = BeautifulSoup(response.text, 'html.parser')
        table = soup.find('table')
        df_aa = pd.read_html(str(table))[0]
    return df_aa

def extract_aa_pka(df:pd.DataFrame):
    series_aa = df.iloc[2:22, 2]
    series_pka = df.iloc[2:22, 7]
    df = pd.concat([series_aa, series_pka], axis=1)
    df.columns = ['Key', 'Value']
    df = df.dropna()
    df['Key'] = df['Key'] + ' pKa'
    return df


def make_deck(df:pd.DataFrame, deck_name:str, package_name:str):
    deck = genanki.Deck(AMINO_ACIDS_ID, deck_name)
    for _, row in df.iterrows():
        note = genanki.Note(model=genanki.BASIC_MODEL, fields=[row['Key'], row['Value']])
        deck.add_note(note)
    genanki.Package(deck).write_to_file(package_name)


def extract_aa_codes(df:pd.DataFrame):
    series_aa = df.iloc[2:22, 1]
    series_code = df.iloc[2:22, 2]
    df = pd.concat([series_aa, series_code], axis=1)
    df.columns = ['Key', 'Value']
    df = df.dropna()
    df['Key'] = df['Key'] + ' Code'
    return df

if __name__ == '__main__':
    df = get_amino_acids()
    df_pka = extract_aa_pka(df)
    make_deck(df_pka, 'Amino Acids pKa', 'amino_acids_pka.apkg')

    df_codes = extract_aa_codes(df)
    make_deck(df_codes, 'Science::Amino Acids', 'amino_acids_codes.apkg')
    print(df_codes)