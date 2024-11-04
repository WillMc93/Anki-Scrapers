from genanki import Model

from anki_ids import DEFINITION_TO_TERM_ID, TERM_TO_DEFINITION_ID

term_2_def_model = Model(
    DEFINITION_TO_TERM_ID,
    'Definition Model',
    fields=[
        {'name': 'Term'},
        {'name': 'Definition'},
    ],
    templates=[
        {
            'name': 'Term to Definition',
            'qfmt': '{{Term}}',
            'afmt': '{{FrontSide}}<hr id="answer">{{Definition}}',
        },
    ],
)

def_2_term_model = Model(
    TERM_TO_DEFINITION_ID,
    'Term Model',
    fields=[
        {'name': 'Definition'},
        {'name': 'Term'},
    ],
    templates=[
        {
            'name': 'Definition to Term',
            'qfmt': '{{Definition}}',
            'afmt': '{{FrontSide}}<hr id="answer">{{Term}}',
        },
    ],
)