from genanki import Model

from .anki_ids import DEFINITION_ID

definition_model = Model(
    DEFINITION_ID,
    'Definition Model',
    fields=[
        {'name': 'Term'},
        {'name': 'Definition'},
    ],
    templates=[
        {
            'name': 'Definition',
            'qfmt': '{{Term}}',
            'afmt': '{{FrontSide}}<hr id="answer">{{Definition}}',
        },
    ],
)
